from glintAPI import glint_api
import argparse
import logging
import os
import sys
#import warnings

#print glintAPI.getImages("this", "works")

def env(*vars, **kwargs):
    """ Try to find the first environnental variable in vars,
        if successful return it.
        Otherwise return the default defined in kwargs.

    """
    for v in vars:
        value = os.environ.get(v)
        if value:
            return value
    return kwargs.get('default', '')


class glintCommands(object):

    def __init__(self, parser_class=argparse.ArgumentParser):
        self.parser_class = parser_class
        self.api = glint_api('api.log', 'logging.DEBUG', 'api.yaml')

    def get_base_parser(self):
        self.parent = self.parser_class(
                prog='glint',
                epilog='See "glint help COMMAND" '
                        'for help on a specific command.',
                add_help=False
        )

        # Global arguments

        self.parent.add_argument('--user-token',
                             default=env('USER_TOKEN'),
                             help='Token used for authentication with the '
                                  'OpenStack Identity service. '
                                  'Defaults to env[USER_TOKEN].')
        
        self.parent.add_argument('--user-tenant',
                             default=env('USER_TENANT'),
                             help='Tenant used for authentication with the '
                                  'OpenStack Identity service. '
                                  'Defaults to env[USER_TENANT].')


        self.parent.add_argument('--json-message',
                             default=env('JSON_MESSAGE'),
                             help='Message used for authentication with the '
                                  'OpenStack Identity service. '
                                  'Defaults to env[JSON_MESSAGE].')

        self.parent.add_argument('--user-id',
                             default=env('USER_ID'),
                             help='User ID used for authentication with the '
                                  'OpenStack Identity service. '
                                  'Defaults to env[USER_ID].')

        self.parent.add_argument('--site-id',
                             default=env('SITE_ID'),
                             help='Site ID used for authentication with the '
                                  'OpenStack Identity service. '
                                  'Defaults to env[SITE_ID].')


        self.parent.add_argument('--site-data',
                             default=env('SITEDATA'),
                             help='Site data used for authentication with the '
                                  'OpenStack Identity service. '
                                  'Defaults to env[SITEDATA].')


        self.parent.add_argument('--ck-type',
                             default=env('CK_TYPE'),
                             help='CK type used for authentication with the '
                                  'OpenStack Identity service. '
                                  'Defaults to env[CK_TYPE].')


        self.parent.add_argument('--cred-data',
                             default=env('CREDDATA'),
                             help='Credential data used for authentication with the '
                                  'OpenStack Identity service. '
                                  'Defaults to env[CREDDATA].')
         

    def getImages(self, args):
        images = self.api.getImages(args.user_token, args.user_tenant,args.user_id)
        if images:
            return images
        else:
            print "ERROR"

    def save(self, args):
        return glintAPI.save(args.json_message, args.user_token, args.user_tenant)

    def credentials(self, args):
        return glintAPI.credentials(args.user_token, args.user_tenant, args.user_id)


    def listSites(self, args):
        return glintAPI.listSites(args.user_token, args.user_tenant)

    def deleteSite(self, args):
        return glintAPI.deleteSite(args.user_token, args.user_tenant, args.user_id, args.site_id)

    def createSite(self, args):
        return glintAPI.createSite(args.user_token, args.user_tenant, args.user_id, args.site_data)

    def deleteCredential(self, args):
        return glintAPI.deleteCredential(args.user_token, args.user_tenant, args.user_id, args.site_id)

    def getCredential(self, args):
        return glintAPI.getCredential(args.user_token, args.user_tenant, args.user_id, args.site_id)

    def hasCredential(self, args):
        return glintAPI.hasCredential(args.user_token, args.user_tenant, args.user_id, args.site_id, args.ck_type)

    def addCredential(self, args):
        return glintAPI.addCredential(args.user_token, args.user_tenant, args.cred_data)


    def get_sub_command_parser(self):

        parser = self.parser_class(
                prog='glint',
                epilog='See "glint help COMMAND" '
                        'for help on a specific command.',
                add_help=False
        )

        subparser = parser.add_subparsers(prog='glint')

        # subparser for the get-images command
        parser_getImages = subparser.add_parser('get-images',
                                                parents=[self.parent], 
                                                help='get images help')
        parser_getImages.set_defaults(func=self.getImages)

        
        # subparser for the save command
        parser_save = subparser.add_parser('save',
                                           parents=[self.parent],
                                           help='save help')
        parser_save.set_defaults(func=self.save)


        # subparser for the credentials command
        parser_credential = subparser.add_parser('credentials',
                                                 parents=[self.parent],
                                                 help='credentials help')
        parser_credential.set_defaults(func=self.credentials)



        # subparser for the list-sites command
        parser_listSites = subparser.add_parser('list-sites',
                                                 parents=[self.parent],
                                                 help='list sites help')
        parser_listSites.set_defaults(func=self.listSites)


        # subparser for the delete-site command
        parser_deleteSite = subparser.add_parser('delete-site',
                                                 parents=[self.parent],
                                                 help='delete site help')
        parser_deleteSite.set_defaults(func=self.deleteSite)


        # subparser for the create-site command
        parser_createSite = subparser.add_parser('create-site',
                                                 parents=[self.parent],
                                                 help='create site help')
        parser_createSite.set_defaults(func=self.createSite)


        # subparser for the delete-credential command
        parser_deleteCredential = subparser.add_parser('delete-credential',
                                                 parents=[self.parent],
                                                 help='delete credential help')
        parser_deleteCredential.set_defaults(func=self.deleteCredential)


        # subparser for the get-credential command
        parser_getCredential = subparser.add_parser('get-credential',
                                                 parents=[self.parent],
                                                 help='get credential help')
        parser_getCredential.set_defaults(func=self.getCredential)


        # subparser for the has-credential command
        parser_hasCredential = subparser.add_parser('has-credential',
                                                 parents=[self.parent],
                                                 help='has credential help')
        parser_hasCredential.set_defaults(func=self.hasCredential)


        # subparser for the add-credential command
        parser_addCredential = subparser.add_parser('add-credential',
                                                 parents=[self.parent],
                                                 help='add credential help')
        parser_addCredential.set_defaults(func=self.addCredential)

        return parser
    

    def main(self, argv):
        self.get_base_parser()

        subcommand_parser = self.get_sub_command_parser()

        command_args = subcommand_parser.parse_args(argv)

#        print command_args.site_data

        print command_args.func(command_args)


def main():
    glintCommands().main(sys.argv[1:])

if __name__=="__main__":
    sys.exit(main())
