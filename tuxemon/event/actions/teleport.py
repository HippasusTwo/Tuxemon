# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2024 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import final

from tuxemon import prepare
from tuxemon.event.eventaction import EventAction
from tuxemon.states.world.worldstate import WorldState

logger = logging.getLogger(__name__)


@final
@dataclass
class TeleportAction(EventAction):
    """
    Teleport the player to a particular map and tile coordinates.

    Script usage:
        .. code-block::

            teleport <map_name>,<x>,<y>

    Script parameters:
        map_name: Name of the map to teleport to.
        x: X coordinate of the map to teleport to.
        y: Y coordinate of the map to teleport to.

    """

    name = "teleport"
    map_name: str
    x: int
    y: int

    def start(self) -> None:
        player = self.session.player
        world = self.session.client.get_state_by_name(WorldState)

        # Check to see if we're also performing a transition. If we are, wait
        # to perform the teleport at the apex of the transition
        # TODO: This only needs to happen once.
        if world.in_transition:
            world.delayed_mapname = self.map_name
            world.delayed_teleport = True
            world.delayed_x = self.x
            world.delayed_y = self.y
        else:
            # If we're not doing a transition, then just do the teleport
            map_path = prepare.fetch("maps", self.map_name)

            if world.current_map is None:
                world.change_map(map_path)

            elif map_path != world.current_map.filename:
                world.change_map(map_path)
                logger.debug(f"Load {map_path}")

            logger.debug(f"Stop {player.slug}'s movements")
            player.cancel_path()

            logger.debug(f"Set {player.slug}'s position")
            logger.debug(f"Tile: ({self.x},{self.y})")
            player.set_position((self.x, self.y))

            logger.debug(f"Unlock {player.slug}'s controls")
            world.unlock_controls()
