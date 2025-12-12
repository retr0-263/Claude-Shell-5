"""
═══════════════════════════════════════════════════════════════════════════
UNIFIED CONFIGURATION LOADER
═══════════════════════════════════════════════════════════════════════════
This module provides a single point of configuration access for all framework
components (Agent, Server, Bot). It handles:
- YAML parsing and validation
- Environment variable overrides
- Configuration versioning
- Change detection and alerts
═══════════════════════════════════════════════════════════════════════════
"""

import yaml
import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION LOADER
# ═══════════════════════════════════════════════════════════════════════════

class ConfigLoader:
    """
    Centralized configuration management for all framework components.
    This is the SINGLE SOURCE OF TRUTH for all configuration.
    """
    
    def __init__(self, config_path: str = "umbrella_config.yaml"):
        """Initialize config loader with path to master config file"""
        self.config_path = Path(config_path)
        self.config = {}
        self.config_hash = None
        self.last_loaded = None
        self.logger = self._setup_logger()
        
        # Load configuration
        self.reload()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for config operations"""
        logger = logging.getLogger("ConfigLoader")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def reload(self) -> bool:
        """
        Reload configuration from file.
        Returns True if config changed, False otherwise.
        """
        try:
            if not self.config_path.exists():
                self.logger.error(f"Config file not found: {self.config_path}")
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                new_config = yaml.safe_load(f)
            
            if not new_config:
                self.logger.error("Config file is empty or invalid YAML")
                return False
            
            # Check if config changed
            new_hash = self._calculate_hash(new_config)
            config_changed = (new_hash != self.config_hash)
            
            self.config = new_config
            self.config_hash = new_hash
            self.last_loaded = datetime.now()
            
            # Apply environment variable overrides
            self._apply_env_overrides()
            
            # Validate configuration
            self._validate_config()
            
            if config_changed:
                self.logger.info("Configuration reloaded successfully")
                return True
            return False
        
        except yaml.YAMLError as e:
            self.logger.error(f"YAML parsing error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return False
    
    def _calculate_hash(self, config: Dict) -> str:
        """Calculate hash of configuration for change detection"""
        config_str = json.dumps(config, sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()
    
    def _apply_env_overrides(self):
        """Apply environment variable overrides to config"""
        # Server overrides
        if os.getenv('RAT_SERVER_IP'):
            self.config['server']['primary_ip'] = os.getenv('RAT_SERVER_IP')
        if os.getenv('RAT_SERVER_PORT'):
            self.config['server']['listen_port'] = int(os.getenv('RAT_SERVER_PORT'))
        if os.getenv('RAT_API_PORT'):
            self.config['server']['api_port'] = int(os.getenv('RAT_API_PORT'))
        
        # Agent overrides
        if os.getenv('RAT_CALLBACK_IP'):
            self.config['agent']['callback_ip'] = os.getenv('RAT_CALLBACK_IP')
        if os.getenv('RAT_CALLBACK_PORT'):
            self.config['agent']['callback_port'] = int(os.getenv('RAT_CALLBACK_PORT'))
        if os.getenv('RAT_ENCRYPTION_KEY'):
            self.config['agent']['encryption_key'] = os.getenv('RAT_ENCRYPTION_KEY')
        
        # Bot overrides
        if os.getenv('RAT_SERVER_URL'):
            self.config['bot']['server_url'] = os.getenv('RAT_SERVER_URL')
        if os.getenv('RAT_BOT_PREFIX'):
            self.config['bot']['whatsapp']['bot_prefix'] = os.getenv('RAT_BOT_PREFIX')
    
    def _validate_config(self):
        """Validate critical configuration values"""
        try:
            # Check required keys
            required_sections = ['server', 'agent', 'bot', 'security']
            for section in required_sections:
                if section not in self.config:
                    self.logger.warning(f"Missing section in config: {section}")
            
            # Validate server config
            if 'server' in self.config:
                server = self.config['server']
                if not (1 <= server.get('listen_port', 4444) <= 65535):
                    self.logger.warning("Invalid server listen_port")
                if not (1 <= server.get('api_port', 5000) <= 65535):
                    self.logger.warning("Invalid server api_port")
            
            # Validate agent config
            if 'agent' in self.config:
                agent = self.config['agent']
                if not (1 <= agent.get('callback_port', 4444) <= 65535):
                    self.logger.warning("Invalid agent callback_port")
                if len(agent.get('encryption_key', '')) < 10:
                    self.logger.warning("Encryption key is too short")
            
            self.logger.info("Configuration validated successfully")
        
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
    
    # ═════════════════════════════════════════════════════════════════════
    # GETTER METHODS
    # ═════════════════════════════════════════════════════════════════════
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation path.
        Example: get('server.listen_port') returns config['server']['listen_port']
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                if isinstance(value, dict):
                    value = value[key]
                else:
                    return default
            return value
        except (KeyError, TypeError):
            return default
    
    def get_server_config(self) -> Dict:
        """Get complete server configuration"""
        return self.config.get('server', {})
    
    def get_agent_config(self) -> Dict:
        """Get complete agent configuration"""
        return self.config.get('agent', {})
    
    def get_bot_config(self) -> Dict:
        """Get complete bot configuration"""
        return self.config.get('bot', {})
    
    def get_security_config(self) -> Dict:
        """Get complete security configuration"""
        return self.config.get('security', {})
    
    def get_features(self) -> Dict:
        """Get all enabled features"""
        return self.config.get('features', {})
    
    def is_feature_enabled(self, feature_path: str) -> bool:
        """Check if a specific feature is enabled"""
        return self.get(f'features.{feature_path}', False)
    
    def get_deployment_profile(self) -> str:
        """Get current deployment profile"""
        return self.config.get('deployment_profile', 'LocalTest')
    
    def get_deployment_config(self, profile: Optional[str] = None) -> Dict:
        """Get deployment mode configuration"""
        if not profile:
            profile = self.get_deployment_profile()
        return self.config.get('deployment_modes', {}).get(profile, {})
    
    # ═════════════════════════════════════════════════════════════════════
    # CONFIGURATION UPDATE & PERSISTENCE
    # ═════════════════════════════════════════════════════════════════════
    
    def update(self, key_path: str, value: Any) -> bool:
        """
        Update a configuration value and persist to disk.
        Returns True if successful, False otherwise.
        """
        try:
            keys = key_path.split('.')
            config = self.config
            
            # Navigate to parent
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            
            # Update value
            old_value = config.get(keys[-1])
            config[keys[-1]] = value
            
            # Persist to disk
            self._save_config()
            
            self.logger.info(
                f"Updated {key_path}: {old_value} -> {value}"
            )
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to update config: {e}")
            return False
    
    def _save_config(self) -> bool:
        """Save current configuration to disk"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
            self.config_hash = self._calculate_hash(self.config)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
            return False
    
    # ═════════════════════════════════════════════════════════════════════
    # CONFIGURATION EXPORT & DEBUG
    # ═════════════════════════════════════════════════════════════════════
    
    def get_status(self) -> Dict:
        """Get configuration status information"""
        return {
            'config_path': str(self.config_path),
            'exists': self.config_path.exists(),
            'last_loaded': str(self.last_loaded) if self.last_loaded else None,
            'config_hash': self.config_hash,
            'deployment_profile': self.get_deployment_profile(),
            'server_ip': self.get('server.primary_ip'),
            'server_port': self.get('server.listen_port'),
            'agent_callback': f"{self.get('agent.callback_ip')}:{self.get('agent.callback_port')}",
            'bot_server_url': self.get('bot.server_url'),
        }
    
    def export_section(self, section: str) -> str:
        """Export specific configuration section as JSON"""
        data = self.config.get(section, {})
        return json.dumps(data, indent=2)
    
    def export_all(self) -> str:
        """Export entire configuration as JSON"""
        return json.dumps(self.config, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
# GLOBAL INSTANCE
# ═══════════════════════════════════════════════════════════════════════════

_global_config = None

def get_config(config_path: str = "umbrella_config.yaml") -> ConfigLoader:
    """
    Get global config instance (singleton pattern).
    First call initializes, subsequent calls return same instance.
    """
    global _global_config
    if _global_config is None:
        _global_config = ConfigLoader(config_path)
    return _global_config

def reload_config() -> bool:
    """Reload global configuration from disk"""
    if _global_config:
        return _global_config.reload()
    return False

# ═══════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def config_get(key_path: str, default: Any = None) -> Any:
    """Get config value using global instance"""
    return get_config().get(key_path, default)

def config_update(key_path: str, value: Any) -> bool:
    """Update config value using global instance"""
    return get_config().update(key_path, value)

def config_status() -> Dict:
    """Get config status using global instance"""
    return get_config().get_status()


if __name__ == "__main__":
    # Test the config loader
    config = get_config()
    print("\n" + "="*70)
    print("CONFIGURATION STATUS")
    print("="*70)
    for key, value in config.get_status().items():
        print(f"  {key}: {value}")
    print("\n" + "="*70)
    print("SAMPLE CONFIG VALUES")
    print("="*70)
    print(f"  Server IP: {config.get('server.primary_ip')}")
    print(f"  Server Port: {config.get('server.listen_port')}")
    print(f"  Agent Callback: {config.get('agent.callback_ip')}:{config.get('agent.callback_port')}")
    print(f"  Bot Server URL: {config.get('bot.server_url')}")
    print(f"  Deployment Profile: {config.get_deployment_profile()}")
    print(f"  Features Enabled: {len([f for f in config.get('features', {}).values() if f])}")
    print("="*70 + "\n")
