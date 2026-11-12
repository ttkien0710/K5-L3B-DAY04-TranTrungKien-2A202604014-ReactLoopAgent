"""Verify real tool calls remain bounded when a model keeps retrying."""
import unittest
from unittest.mock import patch
from agent import run_agent
from bonus.tools import BonusTools
from bonus.test_agent import ScriptedProvider, call, final

class RateBudgetTests(unittest.TestCase):
    def test_persistent_limit_only_executes_twice(self):
        tools = BonusTools(scenario='rate_limit_always')
        model = ScriptedProvider([call(str(i), 'get_vercel_status', {}) for i in range(4)] + [final('Vercel unverified')])
        result = run_agent('Check', model, tools, max_steps=6)
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(tools.calls[('get_vercel_status', 'vercel')], 2)
        observations = [event['result'] for event in result['trace'] if event['event'] == 'tool']
        self.assertFalse(observations[-1]['retriable'])

    def test_long_retry_after_does_not_sleep_or_call_again(self):
        tools = BonusTools()
        tools.execute = unittest.mock.Mock(return_value={'ok': False, 'error': 'RATE_LIMITED', 'retry_after': '120'})
        model = ScriptedProvider([call('a', 'get_vercel_status', {}), call('b', 'get_vercel_status', {}), final('Vercel unverified')])
        with patch('agent.time.sleep') as sleep:
            result = run_agent('Check', model, tools)
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(tools.execute.call_count, 1)
        sleep.assert_not_called()

if __name__ == '__main__':
    unittest.main()
