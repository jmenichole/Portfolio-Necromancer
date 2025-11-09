"""
Portfolio Necromancer - Tests for configuration module
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

import pytest
import os
import tempfile
from portfolio_necromancer.config import Config


def test_default_config():
    """Test default configuration."""
    config = Config(config_file=None)
    
    assert config.get('user.name') is not None
    assert config.get('ai.model') == 'gpt-3.5-turbo'


def test_config_get_set():
    """Test getting and setting config values."""
    config = Config(config_file=None)
    
    # Test get
    name = config.get('user.name')
    assert name is not None
    
    # Test set
    config.set('user.name', 'Test User')
    assert config.get('user.name') == 'Test User'
    
    # Test nested set
    config.set('test.nested.value', 42)
    assert config.get('test.nested.value') == 42


def test_config_save_load():
    """Test saving and loading configuration."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        temp_file = f.name
    
    try:
        # Create and save config
        config1 = Config(config_file=None)
        config1.set('user.name', 'Saved User')
        config1.save(temp_file)
        
        # Load config
        config2 = Config(config_file=temp_file)
        assert config2.get('user.name') == 'Saved User'
    
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
