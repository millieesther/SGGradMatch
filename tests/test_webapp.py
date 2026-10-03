import unittest

from sggradmatch.webapp import render_page, result_html


class WebAppTests(unittest.TestCase):
    def test_template_preserves_css_and_inserts_results(self) -> None:
        page = render_page(results="<p>ready</p>")
        self.assertIn("body{", page)
        self.assertIn("<p>ready</p>", page)

    def test_empty_form_uses_placeholders_not_sample_values(self) -> None:
        page = render_page()
        self.assertIn('placeholder="e.g. business analytics"', page)
        self.assertNotIn('value="business analytics"', page)

    def test_submitted_values_are_preserved_and_escaped(self) -> None:
        page = render_page(
            {
                "academic_background": 'business & <analytics>',
                "career_goal": "data scientist",
                "preferred_mode": "part-time",
            }
        )
        self.assertIn('value="business &amp; &lt;analytics&gt;"', page)
        self.assertIn('value="part-time" selected', page)
        self.assertNotIn('value="full-time" selected', page)

    def test_select_and_inputs_share_one_height(self) -> None:
        page = render_page()
        self.assertIn("input,select{box-sizing:border-box;height:42px", page)

    def test_abstention_message_is_escaped(self) -> None:
        rendered = result_html({"status": "abstain", "message": "Need <two> programmes"})
        self.assertIn("Need &lt;two&gt; programmes", rendered)


if __name__ == "__main__":
    unittest.main()
