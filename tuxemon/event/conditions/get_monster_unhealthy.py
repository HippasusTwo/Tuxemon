# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2024 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
from __future__ import annotations

import logging

from tuxemon.combat import has_status
from tuxemon.event import MapCondition, get_npc
from tuxemon.event.eventcondition import EventCondition
from tuxemon.session import Session

logger = logging.getLogger(__name__)


class CharHasWeakenedMon(EventCondition):
    """
    Check to see the character has at least one tuxemon, and a tuxemon in their
    party are defeated.

    Script usage:
        .. code-block::

            is  <character>

    Script parameters:
        character: Either "player" or character slug name (e.g. "npc_maple")

    """

    name = "get_monster_unhealthy"

    def test(self, session: Session, condition: MapCondition) -> bool:
        character = get_npc(session, condition.parameters[0])
        if character is None:
            logger.error(f"{condition.parameters[0]} not found")
            return False

        if character.monsters:
            for mon in character.monsters:
                if mon.current_hp <= 10:
                    return True
        return False
