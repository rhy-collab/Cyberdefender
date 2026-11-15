import unittest
from radar import dns_observation, header_observations, report

class EvidenceTests(unittest.TestCase):
    def test_malformed_answers_are_not_passes(self):
        for answers in (None, {}, [None], [{'type':16,'data':42}]):
            self.assertEqual(dns_observation('spf', {'Status':0,'Answer':answers})['status'],'unable_to_assess')

    def test_failure_is_not_absence(self):
        for status in (2, 5):
            self.assertEqual(dns_observation('spf', {'Status': status})['status'], 'unable_to_assess')

    def test_truncated_answer_is_incomplete(self):
        self.assertEqual(dns_observation('spf', {'Status': 0, 'TC': True})['status'], 'unable_to_assess')

    def test_missing_is_not_critical(self):
        o = dns_observation('spf', {'Status': 0})
        self.assertEqual(o['classification'], 'configuration_review')
        self.assertEqual(o['severity'], 'unrated')

    def test_dmarc_monitoring_not_vulnerability(self):
        o = dns_observation('dmarc', {'Status': 0, 'Answer': [{'type':16,'data':'"v=DMARC1; p=none"'}]})
        self.assertEqual(o['status'], 'observed')
        self.assertIn('not proof', o['interpretation'])

    def test_multiple_spf_records(self):
        o = dns_observation('spf', {'Status':0,'Answer':[{'type':16,'data':'"v=spf1 -all"'},{'type':16,'data':'"v=spf1 ~all"'}]})
        self.assertEqual(o['classification'], 'configuration_review')

    def test_headers_case_insensitive(self):
        obs = header_observations(200, {'X-Content-Type-Options':'nosniff'})
        self.assertEqual(next(o for o in obs if o['check']=='x-content-type-options')['evidence'],'nosniff')

    def test_error_response_not_missing_controls(self):
        self.assertTrue(all(o['status']=='unable_to_assess' for o in header_observations(503, {})))

    def test_report_escapes_untrusted_evidence(self):
        self.assertNotIn('<script>', report([{'check':'x','status':'observed','evidence':'<script>','interpretation':'example'}]))

    def test_txt_chunks_are_joined(self):
        o=dns_observation('spf',{'Status':0,'Answer':[{'type':16,'data':'"v=spf1 " "-all"'}]})
        self.assertEqual(o['evidence'], ['v=spf1 -all'])

if __name__ == '__main__': unittest.main()
