
Plone 2.5 Notes
===============

Adding GetPaid content fields to main_template.pt
-------------------------------------------------
If you'd like to display the Content fields underneath any content-types
that are marked by the user as Payable, you can modify main_template.pt
and add the following snippet, which brings in the Viewlet Manager.  The
Viewlet Manager (via settings in content.zcml) brings in a different
viewlet depending on which type of Payable content you're viewing since
each may have a different set of fields:

For example, in main_template.pt after this snippet:

    <metal:sub metal:define-slot="sub">
      <metal:discussion use-macro="here/viewThreadsAtBottom/macros/discussionView" />
    </metal:sub>

add:

    <tal:plonegetpaid_view_manager tal:define="
            global plone_view context/@@plone;
            global view nocall:view | nocall:plone_view;
            foo plone_view/globalize;">
            
      <div tal:replace="structure provider:content_widget_manager" />
      
    </tal:plonegetpaid_view_manager>
