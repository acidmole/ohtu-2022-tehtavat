*** Settings ***
Resource  resource.robot
Test Setup  Input New Command And Create User

*** Test Cases ***
Register With Valid Username And Password
    Input Credentials  karipaakko  kuolema8
    Output Should Contain  New user registered

Register With Already Taken Username And Valid Password
    Input Credentials  karipaakko  pahkasik4
    Input New Command And Create User
    Input Credentials  karipaakko  p555sösöslkf
    Output Should Contain  User with username karipaakko already exists

Register With Too Short Username And Valid Password
    Input Credentials  qp  p555sösöslkf
    Output Should Contain  Invalid username

Register With Valid Username And Too Short Password
    Input Credentials  karipaakko  4chren
    Output Should Contain  Invalid password


Register With Valid Username And Long Enough Password Containing Only Letters
        Input Credentials  karipaakko  mikkoachren
        Output Should Contain  Invalid password


*** Keywords ***
Input New Command And Create User
    Input New Command