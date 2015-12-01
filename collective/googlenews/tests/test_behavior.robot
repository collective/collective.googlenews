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
    Update  World Cup
    Page Should Contain  Changes saved
    Page Should Contain Element  xpath=//meta[@name='standout']
    Page Should Contain Element  xpath=//meta[@name='news_keywords']

    # creating a new one will be voided
    Go to Homepage
    Create  Read all about it!
    Page Should Contain  There were some errors
    Page Should Contain  Can't mark this news article as standout
    Page Should Contain  There are already seven marked in the past calendar week

    Click Link  Extra! Extra!
    Delete

*** Keywords ***

Click Add Dexterity Item
    Open Add New Menu
    Click Link  css=a#dexterity-item
    Page Should Contain  Dexterity Item

Create
    [arguments]  ${title}

    Click Add Dexterity Item
    Input Text  css=${title_selector}  ${title}
    Click Link  Google News
    Select Checkbox  css=${standout_journalism_selector}
    Click Button  Save

Update
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
