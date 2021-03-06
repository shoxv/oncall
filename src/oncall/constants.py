# Copyright (c) LinkedIn Corporation. All rights reserved. Licensed under the BSD-2 Clause license.
# See LICENSE in the project root for license information.

EMAIL_SUPPORT = 'email'
SMS_SUPPORT = 'sms'
CALL_SUPPORT = 'call'
IM_SUPPORT = 'im'

ONCALL_REMINDER = 'oncall_reminder'
OFFCALL_REMINDER = 'offcall_reminder'
EVENT_CREATED = 'event_created'
EVENT_EDITED = 'event_edited'
EVENT_DELETED = 'event_deleted'
EVENT_SWAPPED = 'event_swapped'
EVENT_SUBSTITUTED = 'event_substituted'

TEAM_CREATED = 'team_created'
TEAM_EDITED = 'team_edited'
TEAM_DELETED = 'team_deleted'
ROSTER_CREATED = 'roster_created'
ROSTER_EDITED = 'roster_edited'
ROSTER_USER_ADDED = 'roster_user_added'
ROSTER_USER_EDITED = 'roster_user_edited'
ROSTER_USER_DELETED = 'roster_user_deleted'
ROSTER_DELETED = 'roster_deleted'
ADMIN_CREATED = 'admin_created'
ADMIN_DELETED = 'admin_deleted'

DEFAULT_ROLES = None
DEFAULT_MODES = None
DEFAULT_TIMES = None


def init(config):
    global DEFAULT_ROLES
    global DEFAULT_MODES
    global DEFAULT_TIMES
    DEFAULT_ROLES = config['notifications']['default_roles']
    DEFAULT_MODES = config['notifications']['default_modes']
    DEFAULT_TIMES = config['notifications']['default_times']