from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class GameState:
    x: int = 0
    y: int = 0
    score: int = 0
    health: int = 3
    ticks: int = 0


def step(state: GameState, command: str) -> GameState:
    """Deterministic grid-game transition used as the first reproducible gameplay slice."""
    command = command.strip().lower()
    moves = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
    if command in moves:
        dx, dy = moves[command]
        return replace(state, x=state.x + dx, y=state.y + dy, ticks=state.ticks + 1)
    if command == "collect":
        return replace(state, score=state.score + 10, ticks=state.ticks + 1)
    if command == "damage":
        return replace(state, health=max(0, state.health - 1), ticks=state.ticks + 1)
    if command == "wait":
        return replace(state, ticks=state.ticks + 1)
    raise ValueError(f"unsupported command: {command}")


def replay(commands: list[str], initial: GameState | None = None) -> GameState:
    state = initial or GameState()
    for command in commands:
        state = step(state, command)
    return state


def is_game_over(state: GameState) -> bool:
    return state.health == 0
