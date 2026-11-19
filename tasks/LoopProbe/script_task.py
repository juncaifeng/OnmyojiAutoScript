# This Python file uses the following encoding: utf-8
"""Hidden task that reads a loop-scheduling probe and stores the result.

The loop scheduler runs this task through the normal task loader, then reads
``log/loop_probe_<config>.json``. It is not part of the user-facing task menu.
"""
import json
from datetime import datetime

from module.exception import TaskEnd
from module.runtime import data_path
from tasks.GameUi.game_ui import GameUi
from tasks.GameUi.page import page_realm_raid
from tasks.RealmRaid.assets import RealmRaidAssets


class ScriptTask(GameUi, RealmRaidAssets):
    def run(self):
        probe = getattr(self.config.script.loop.probe, 'value', self.config.script.loop.probe)
        payload = {
            'probe': probe,
            'time': datetime.now().isoformat(timespec='seconds'),
        }
        try:
            if probe == 'realm_raid_ticket':
                self.goto_page(page_realm_raid)
                self.screenshot()
                current, remaining, total = self.O_NUMBER.ocr(self.device.image)
                payload.update({
                    'ok': True,
                    'value': int(current),
                    'remaining': int(remaining),
                    'total': int(total),
                })
            else:
                # `always` and future probes that need no game state
                payload.update({'ok': True, 'value': 1})
        except Exception as error:
            payload.update({'ok': False, 'error': str(error)})

        target = data_path('log', f'loop_probe_{self.config.config_name}.json')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        raise TaskEnd
