from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class VerkkomaksutPaymentButton(object):
    def __init__(self, context, request, step, manager):
        self.context = context
        self.request = request
        self.step = step
        self.manager = manager

    def __call__(self):
        return "VerkkomaksutButton"
