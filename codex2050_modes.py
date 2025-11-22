
import os
from dataclasses import dataclass
from enum import IntEnum


class CodexStage(IntEnum):
    STAGE_1 = 1
    STAGE_2 = 2
    STAGE_3 = 3
    STAGE_4 = 4
    STAGE_5 = 5
    STAGE_6 = 6


@dataclass
class Codex2050Config:
    max_stage: int = 1
    openai_enabled: bool = False

    @property
    def stage(self) -> int:
        return int(self.max_stage)

    @property
    def stage1_online_echo(self) -> bool:
        return self.stage >= CodexStage.STAGE_1

    @property
    def stage2_protection_filter(self) -> bool:
        return self.stage >= CodexStage.STAGE_2

    @property
    def stage3_auto_reply(self) -> bool:
        return self.stage >= CodexStage.STAGE_3

    @property
    def stage4_archiv_hook(self) -> bool:
        return self.stage >= CodexStage.STAGE_4

    @property
    def stage5_monitoring(self) -> bool:
        return self.stage >= CodexStage.STAGE_5

    @property
    def stage6_full_ai(self) -> bool:
        return self.stage >= CodexStage.STAGE_6 and self.openai_enabled


def load_config() -> Codex2050Config:
    stage_raw = os.getenv("CODEX2050_STAGE", "1")
    try:
        stage = int(stage_raw)
    except ValueError:
        stage = 1

    stage = max(1, min(6, stage))

    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    openai_enabled = bool(openai_key)

    return Codex2050Config(max_stage=stage, openai_enabled=openai_enabled)
