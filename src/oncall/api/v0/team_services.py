# Copyright (c) LinkedIn Corporation. All rights reserved. Licensed under the BSD-2 Clause license.
# See LICENSE in the project root for license information.

from urllib import unquote
from falcon import HTTPError, HTTP_201
from ujson import dumps as json_dumps
from ...auth import login_required, check_team_auth
from ...utils import load_json_body

from ... import db


def on_get(req, resp, team):
    """
    Get list of services mapped to a team
    """
    team = unquote(team)
    connection = db.connect()
    cursor = connection.cursor()
    cursor.execute('''SELECT `service`.`name` FROM `service`
                      JOIN `team_service` ON `team_service`.`service_id`=`service`.`id`
                      JOIN `team` ON `team`.`id`=`team_service`.`team_id`
                      WHERE `team`.`name`=%s''',
                   team)
    data = [r[0] for r in cursor]
    cursor.close()
    connection.close()
    resp.body = json_dumps(data)


@login_required
def on_post(req, resp, team):
    """
    Create team to service mapping
    """
    team = unquote(team)
    check_team_auth(team, req)
    data = load_json_body(req)

    service = data['name']
    connection = db.connect()
    cursor = connection.cursor()
    try:
        # TODO: allow many to many mapping for team/service?
        cursor.execute('''SELECT `team`.`name` from `team_service`
                          JOIN `team` ON `team`.`id` = `team_service`.`team_id`
                          JOIN `service` ON `service`.`id` = `team_service`.`service_id`
                          WHERE `service`.`name` = %s''', service)
        claimed_team = [r[0] for r in cursor]
        if claimed_team:
            raise HTTPError('422 Unprocessable Entity',
                            'IntegrityError',
                            'service "%s" alread claimed by team "%s"' % (service, claimed_team[0]))

        cursor.execute('''INSERT INTO `team_service` (`team_id`, `service_id`)
                          VALUES (
                              (SELECT `id` FROM `team` WHERE `name`=%s),
                              (SELECT `id` FROM `service` WHERE `name`=%s)
                          )''',
                       (team, service))
        connection.commit()
    except db.IntegrityError as e:
        err_msg = str(e.args[1])
        if err_msg == 'Column \'service_id\' cannot be null':
            err_msg = 'service "%s" not found' % service
        elif err_msg == 'Column \'team_id\' cannot be null':
            err_msg = 'team "%s" not found' % team
        elif 'Duplicate entry' in err_msg:
            err_msg = 'service name "%s" is already associated with team %s' % (service, team)
        raise HTTPError('422 Unprocessable Entity', 'IntegrityError', err_msg)
    finally:
        cursor.close()
        connection.close()

    resp.status = HTTP_201
