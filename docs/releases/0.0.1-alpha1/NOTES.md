# Release notes
## Release version and status

Version: 0.0.1-alpha1
Status: Alpha

## Notes
All these features were tested manually and suppose to work as expected, but
because of release status it's not guaranteed:

- [X] Deployment tasks are work synchronous
- [X] Status updates are comes to UI
- [X] IPMI commands
- [X] SSH keys export(to be able to place on node)
- [X] Pagination for views contain multiple items
- [X] Working and tested example profile for Ubuntu 16.04 LTS
- [X] UI tested on Google Chrome, recent Firefox, Safari
- [X] UI-based workflow. i.e. it's possible to perform all the action from UI

## Known issues

- Deployment creation could raise unhandled exception not present in UI on
    creating deployment if the network server suppose to be is not created.
- Status of deployment could be set to 'complete' state before achieving 100%
    progress.
- In alpha1 version JS errors are handler with alert() function, will be changed
    by 0.0.1-beta1.
- In alpha1 there's no way to view network details though WebUI, will be changed
    by 0.0.1-beta1.
- In alpha1 there's no way to updated any object details except some specific
    ones through WebUI, will be changed by 0.0.1-beta1.
