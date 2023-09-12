# Movix Django Admin panel

## What is it?

An admin panel for controlling the Movix.

Now there are components:

-   movies
-   notifications

## How to use it?

1. Clone main repo of [movix](https://github.com/stranded-in-python/movix)

3. Run `make init && make admin` to startup the service.

## Tell me more about...

### Notifications

You can control user's notifications by creating new ones, setting recurring tasks and manually launching them.

#### Creating a notification

To create a new notification, you'll need to:

-   Create or select existing pool of recipients `UserGroup`
-   Create a new template. HTML and plain text are supported.
-   Create a new notification

#### Set a recurring task

To set a recurring task, you'll need to create a new entry for `NotificationCrons`. Period is set by a [cron string](https://en.wikipedia.org/wiki/Cron)

#### Manually launch a notification

Just select a notificaion from the list and launch it by 'Send notifications' admin action.

## Authors

-   [Stranded in Python](https://github.com/stranded-in-python)
