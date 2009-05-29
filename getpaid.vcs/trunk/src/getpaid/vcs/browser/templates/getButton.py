form = cgi.FieldStorage()
formvals.append = {"p1": form['p1'].value,
                    "p2": form['p2'].value,
                    "p3": form['p3'].value,
                    "p4": form['p4'].value,
                    "p5": form['p5'].value,
                    }
_button_form = """<form style="display:inline;" action="https://www.vcs.co.za/vvonline/ccform.asp" method="post" id="vcs-button">
                            <input type="hidden" name="p1" value="%(p1)s" />
                            <input type="hidden" name="p2" value="%(p2)s" />
                            <input type="hidden" name="p3" value="%(p3)s" />
                            <input type="hidden" name="p4" value="%(p4)s" />
                            <input type="hidden" name="p5" value="%(p5)s" />
                            <input type="submit"
                                name="submit"
                                value="Proceed to Payment Page" />
                            </form>
                            """
return _button_form % formvals
