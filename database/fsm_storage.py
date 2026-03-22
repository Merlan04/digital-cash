"""
FSM Storage в БД (вместо MemoryStorage)
Все данные сохраняются в БД и не потеряются при перезагрузке
"""

import json
from typing import Any, Dict, Optional
from aiogram.fsm.storage.base import BaseStorage, StateKey
from aiogram.fsm.state import State
from database.db import save_fsm_state, get_fsm_state, delete_fsm_state


class DatabaseFSMStorage(BaseStorage):
    """FSM Storage в SQLite БД"""

    async def set_state(self, key: StateKey, state: Optional[State]) -> None:
        """Сохранить состояние"""
        user_id = key.user_id
        state_str = state.state if state else None
        save_fsm_state(user_id, state_str, {})

    async def get_state(self, key: StateKey) -> Optional[str]:
        """Получить состояние"""
        state, _ = get_fsm_state(key.user_id)
        return state

    async def set_data(self, key: StateKey, data: Dict[str, Any]) -> None:
        """Сохранить данные состояния"""
        user_id = key.user_id
        state, _ = get_fsm_state(user_id)
        save_fsm_state(user_id, state, data)

    async def get_data(self, key: StateKey) -> Dict[str, Any]:
        """Получить данные состояния"""
        _, data = get_fsm_state(key.user_id)
        return data if data else {}

    async def close(self) -> None:
        """Закрыть хранилище (если нужно)"""
        pass
