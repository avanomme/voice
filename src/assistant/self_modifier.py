#!/usr/bin/env python3
"""
Self-Modification System for Voice Assistant
Allows the AI to safely modify its own program files with user permission
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import json
from datetime import datetime

from memory_manager import get_memory_manager

class SelfModifier:
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize self-modification system"""
        if project_root is None:
            self.project_root = Path.home() / "voice-assistant"
        else:
            self.project_root = project_root

        self.memory = get_memory_manager()
        self.logger = logging.getLogger(__name__)

        # Create backup directory
        self.backup_dir = self.project_root / "backups"
        self.backup_dir.mkdir(exist_ok=True)

        # Files that can be safely modified
        self.modifiable_files = {
            "src/assistant/voice_models.py",
            "src/assistant/assistant_logic.py",
            "src/assistant/web_voice_assistant.py",
            "src/assistant/memory_manager.py",
            "src/assistant/self_modifier.py",
            ".claude/settings.json",
            "docs/",
            "memory/"
        }

    def request_permission(self, action: str, files: List[str], reason: str) -> bool:
        """Request user permission for file modification"""
        permission_key = f"permission_{action}_{hash('_'.join(files))}"

        # Check if permission already granted
        existing_permission = self.memory.recall(permission_key)
        if existing_permission:
            return existing_permission.get('granted', False)

        # In a real implementation, this would prompt the user
        # For now, we'll log the request and assume permission for safe operations
        self.logger.info(f"Permission requested: {action} on {files} - Reason: {reason}")

        # Auto-grant for safe operations
        safe_actions = ['backup', 'read', 'update_config', 'add_memory']
        granted = action in safe_actions

        # Store permission decision
        self.memory.remember(permission_key, {
            'granted': granted,
            'action': action,
            'files': files,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })

        return granted

    def backup_file(self, file_path: Path) -> Optional[Path]:
        """Create backup of a file before modification"""
        try:
            if not file_path.exists():
                return None

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"{file_path.name}_{timestamp}.backup"

            shutil.copy2(file_path, backup_path)
            self.logger.info(f"Backed up {file_path} to {backup_path}")
            return backup_path

        except Exception as e:
            self.logger.error(f"Failed to backup {file_path}: {e}")
            return None

    def modify_file(self, file_path: str, content: str, reason: str) -> bool:
        """Safely modify a program file"""
        try:
            full_path = self.project_root / file_path

            # Check if file is modifiable
            if not any(str(full_path).endswith(modifiable) or modifiable in str(full_path)
                      for modifiable in self.modifiable_files):
                self.logger.error(f"File {file_path} is not in modifiable list")
                return False

            # Request permission
            if not self.request_permission('modify', [file_path], reason):
                self.logger.error(f"Permission denied to modify {file_path}")
                return False

            # Create backup
            backup_path = self.backup_file(full_path)
            if backup_path is None and full_path.exists():
                self.logger.error(f"Failed to backup {file_path}")
                return False

            # Write new content
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)

            self.logger.info(f"Modified {file_path}: {reason}")

            # Remember the modification
            self.memory.remember(f"modification_{file_path}_{datetime.now().isoformat()}", {
                'file': file_path,
                'reason': reason,
                'backup': str(backup_path) if backup_path else None,
                'timestamp': datetime.now().isoformat()
            })

            return True

        except Exception as e:
            self.logger.error(f"Failed to modify {file_path}: {e}")
            return False

    def add_to_file(self, file_path: str, content: str, position: str = 'end', reason: str = '') -> bool:
        """Add content to an existing file"""
        try:
            full_path = self.project_root / file_path

            if not full_path.exists():
                return self.modify_file(file_path, content, reason)

            # Read existing content
            with open(full_path, 'r') as f:
                existing_content = f.read()

            # Determine new content based on position
            if position == 'start':
                new_content = content + '\n' + existing_content
            else:  # end
                new_content = existing_content + '\n' + content

            return self.modify_file(file_path, new_content, reason)

        except Exception as e:
            self.logger.error(f"Failed to add to {file_path}: {e}")
            return False

    def update_config(self, config_path: str, updates: Dict[str, Any], reason: str) -> bool:
        """Update JSON configuration file"""
        try:
            full_path = self.project_root / config_path

            # Request permission
            if not self.request_permission('update_config', [config_path], reason):
                return False

            # Read existing config
            config = {}
            if full_path.exists():
                with open(full_path, 'r') as f:
                    config = json.load(f)

            # Apply updates
            def deep_update(base_dict, update_dict):
                for key, value in update_dict.items():
                    if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                        deep_update(base_dict[key], value)
                    else:
                        base_dict[key] = value

            deep_update(config, updates)

            # Write updated config
            return self.modify_file(config_path, json.dumps(config, indent=2), reason)

        except Exception as e:
            self.logger.error(f"Failed to update config {config_path}: {e}")
            return False

    def install_skill(self, skill_name: str, skill_code: str, description: str) -> bool:
        """Install a new skill/capability"""
        try:
            skill_path = f"src/assistant/skills/{skill_name}.py"

            if not self.request_permission('install_skill', [skill_path], f"Install skill: {description}"):
                return False

            # Create skills directory
            skills_dir = self.project_root / "src" / "assistant" / "skills"
            skills_dir.mkdir(parents=True, exist_ok=True)

            # Create __init__.py if it doesn't exist
            init_file = skills_dir / "__init__.py"
            if not init_file.exists():
                init_file.write_text("")

            # Write skill file
            success = self.modify_file(skill_path, skill_code, f"Install skill: {skill_name}")

            if success:
                # Update skills registry
                self.memory.remember(f"skill_{skill_name}", {
                    'name': skill_name,
                    'description': description,
                    'path': skill_path,
                    'installed_at': datetime.now().isoformat()
                })

            return success

        except Exception as e:
            self.logger.error(f"Failed to install skill {skill_name}: {e}")
            return False

    def get_modification_history(self) -> List[Dict]:
        """Get history of all modifications"""
        memories = self.memory.get_all_memories()
        modifications = []

        for key, value in memories.items():
            if key.startswith('modification_'):
                modifications.append(value)

        return sorted(modifications, key=lambda x: x.get('timestamp', ''), reverse=True)

    def rollback_modification(self, modification_id: str) -> bool:
        """Rollback a specific modification"""
        try:
            modification = self.memory.recall(modification_id)
            if not modification or not modification.get('backup'):
                return False

            backup_path = Path(modification['backup'])
            file_path = self.project_root / modification['file']

            if backup_path.exists():
                shutil.copy2(backup_path, file_path)
                self.logger.info(f"Rolled back {modification['file']}")
                return True

            return False

        except Exception as e:
            self.logger.error(f"Failed to rollback {modification_id}: {e}")
            return False

# Global self-modifier instance
_self_modifier: Optional[SelfModifier] = None

def get_self_modifier() -> SelfModifier:
    """Get or create the global self-modifier instance"""
    global _self_modifier
    if _self_modifier is None:
        _self_modifier = SelfModifier()
    return _self_modifier