# -*- coding: utf-8 -*-

import os
import sys
from app import create_app, db
from app.models import User, Role, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


def make_shell_content():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)

manager.add_command('shell', Shell(make_context=make_shell_content))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unittest."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
        # sys.exit(subprocess.call(sys.argv))
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    print COV
    if COV:
        COV.stop()
        COV.save()
        print 'Coverage Summary: '
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print 'HTML version: file://%s/index.html' % covdir
        COV.erase()

if __name__ == '__main__':
    manager.run()
