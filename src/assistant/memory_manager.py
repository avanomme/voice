#!/usr/bin/env python3
"""
Memory Manager for Voice Assistant
Handles persistent storage of user information, preferences, and conversation history
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

class MemoryManager:
    def __init__(self, memory_dir: Optional[Path] = None):
        """Initialize memory manager"""
        if memory_dir is None:
            self.memory_dir = Path.home() / "voice-assistant" / "memory"
        else:
            self.memory_dir = memory_dir

        self.memory_dir.mkdir(exist_ok=True)
        self.db_path = self.memory_dir / "memory.db"
        self.logger = logging.getLogger(__name__)

        self._init_database()

    def _init_database(self):
        """Initialize SQLite database for memory storage"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(category, key)
                )
            """)

    def remember(self, key: str, value: Any) -> bool:
        """Store a piece of information"""
        try:
            value_str = json.dumps(value) if not isinstance(value, str) else value

            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO user_memory (key, value, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (key, value_str))

            self.logger.info(f"Remembered: {key}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to remember {key}: {e}")
            return False

    def recall(self, key: str) -> Optional[Any]:
        """Retrieve a piece of information"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT value FROM user_memory WHERE key = ?", (key,)
                )
                result = cursor.fetchone()

                if result:
                    try:
                        return json.loads(result[0])
                    except json.JSONDecodeError:
                        return result[0]

            return None
        except Exception as e:
            self.logger.error(f"Failed to recall {key}: {e}")
            return None

    def forget(self, key: str) -> bool:
        """Remove a piece of information"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM user_memory WHERE key = ?", (key,))

            self.logger.info(f"Forgot: {key}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to forget {key}: {e}")
            return False

    def save_conversation(self, session_id: str, role: str, content: str, metadata: Dict = None):
        """Save conversation message"""
        try:
            metadata_str = json.dumps(metadata) if metadata else None

            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO conversations (session_id, role, content, metadata)
                    VALUES (?, ?, ?, ?)
                """, (session_id, role, content, metadata_str))

        except Exception as e:
            self.logger.error(f"Failed to save conversation: {e}")

    def get_conversation_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Get conversation history for a session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT role, content, timestamp, metadata
                    FROM conversations
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (session_id, limit))

                conversations = []
                for row in cursor.fetchall():
                    metadata = json.loads(row[3]) if row[3] else {}
                    conversations.append({
                        'role': row[0],
                        'content': row[1],
                        'timestamp': row[2],
                        'metadata': metadata
                    })

                return list(reversed(conversations))

        except Exception as e:
            self.logger.error(f"Failed to get conversation history: {e}")
            return []

    def set_preference(self, category: str, key: str, value: Any):
        """Set user preference"""
        try:
            value_str = json.dumps(value) if not isinstance(value, str) else value

            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO preferences (category, key, value)
                    VALUES (?, ?, ?)
                """, (category, key, value_str))

        except Exception as e:
            self.logger.error(f"Failed to set preference {category}.{key}: {e}")

    def get_preference(self, category: str, key: str, default=None):
        """Get user preference"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT value FROM preferences
                    WHERE category = ? AND key = ?
                """, (category, key))

                result = cursor.fetchone()
                if result:
                    try:
                        return json.loads(result[0])
                    except json.JSONDecodeError:
                        return result[0]

            return default
        except Exception as e:
            self.logger.error(f"Failed to get preference {category}.{key}: {e}")
            return default

    def get_all_memories(self) -> Dict[str, Any]:
        """Get all stored memories"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT key, value FROM user_memory")
                memories = {}

                for row in cursor.fetchall():
                    try:
                        memories[row[0]] = json.loads(row[1])
                    except json.JSONDecodeError:
                        memories[row[0]] = row[1]

                return memories
        except Exception as e:
            self.logger.error(f"Failed to get all memories: {e}")
            return {}

# Global memory manager instance
_memory_manager: Optional[MemoryManager] = None

def get_memory_manager() -> MemoryManager:
    """Get or create the global memory manager instance"""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = MemoryManager()
    return _memory_manager