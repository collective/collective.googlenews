*** Settings ***

Documentation  Test content creation and validation with fields from the Google News behavior
Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py

Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${title_selector}  input#form-widgets-IDublinCore-title
${standout_journalism_selector}  input#form-widgets-IGoogleNews-standout_journalism-0
${news_keywords_selector}  textarea#form-widgets-IGoogleNews-news_keywords

*** Test Cases ***

Test CRUD
    Enable Autologin as  Site Administrator
    Go to Homepage

    # at this point we already have 6 news articles marked as standout
    # we can add another one
    Create  Extra! Extra!
    Page Should Contain  Item created
    Page Should Contain Element  xpath=//meta[@name='standout']
    Page Should Not Contain Element  xpath=//meta[@name='news_keywords']

    Workflow Publish

    # we can also edit it
    Add Keywords  World Cup
    Page Should Contain  Changes saved
    Page Should Contain Element  xpath=//meta[@name='standout']
    Page Should Contain Element  xpath=//meta[@name='news_keywords']

    # creating a new one is allowed
    Go to Homepage
    Create  Read all about it!
    Page Should Contain  Item created
    Page Should Contain Element  xpath=//meta[@name='standout']
    Page Should Not Contain Element  xpath=//meta[@name='news_keywords']

    # but no workflow transition is allowed
    Page Should Not Contain Element  css=#workflow-transition-publish
    Page Should Contain  This item is marked as standout journalism but there are already 7 items marked and published in the past calendar week.
    Page Should Contain  The "Publish" workflow transition will be disabled on this item until this situation changes.

    # remove one item from the standout journalism
    Click Link  Extra! Extra!
    Click Link  link=Edit
    Unmark As Standout Journalism
    Click Button  Save

    # now the transition is available for the other
    Click Link  Read all about it!
    Page Should Contain Element  css=#workflow-transition-publish
    Page Should Not Contain  This item is marked as standout journalism but there are already 7 items marked and published in the past calendar week.
    Page Should Not Contain  The "Publish" workflow transition will be disabled on this item until this situation changes.

    Workflow Publish

    Click Link  Extra! Extra!
    Delete

*** Keywords ***

Click Add Dexterity Item
    Open Add New Menu
    Click Link  css=a#dexterity-item
    Page Should Contain  Dexterity Item

Mark As Standout Journalism
    Click Link  Google News
    Select Checkbox  css=${standout_journalism_selector}

Unmark As Standout Journalism
    Click Link  Google News
    Unselect Checkbox  css=${standout_journalism_selector}

Create
    [arguments]  ${title}

    Click Add Dexterity Item
    Input Text  css=${title_selector}  ${title}
    Mark As Standout Journalism
    Click Button  Save

Add Keywords
    [arguments]  ${news_keywords}

    Click Link  link=Edit
    Click Link  Google News
    Input Text  css=${news_keywords_selector}  ${news_keywords}
    Click Button  Save

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Delete
    Page Should Contain  Plone site
