"""File containing the flask_restx models needed to generate the swagger docs.

Each of the following functions corresponds to an endpoint.

`get_collection_models`
`get_overview_models`
`get_list_models`
`get_info_models`
`get_backup_models`
`get_search_models`
`get_edit_models`
`get_unbackup_models`
`get_delete_models`
`get_listbackups_models`

"""

from flask_restx import fields

def get_collection_models(api) -> dict[str, object]:
    collection_input_model = api.model("AddCollection", {
        "name":              fields.String(required=True, description="The unique name of the collection", default="Unique Name"),
        "description":       fields.String(required=True, description="The description of the collection", default="The description of the collection"),
        "creation_date":     fields.String(required=False, description="Optional creation date. Set to current time if not set", default="1960-06-01 15:31:10"),
        "modification_date": fields.String(required=False, description="Optional modification date. Set to current time if not set", default="1960-06-01 15:31:10"),
        "updated":           fields.Boolean(required=False, description="Optional mark if the collection is up to date or not. Default to true", default=True)
    }, strict=True) #This makes flask_restx automatically input validate to enforce only these parameters
    
    collection_success_model = api.model("AddCollectionSuccess", {
        "errors":  fields.Nested(api.model("NoError", {})),
        "message": fields.String(default="Collection Created Successfully")
    })

    collection_failure_model = api.model("AddCollectionFailure", {
        "errors":  fields.Raw(   default='{"CollectionAlreadyExistsError": "Collection with name \'name\' already exists"}'),
        "message": fields.String(default="No Collection Was Created")
    })

    return {
        "input": collection_input_model,
        "success": collection_success_model,
        "failure": collection_failure_model
    }

def get_overview_models(api) -> dict[str, object]:
    overview_success_model = api.model("OverviewSuccess", {
        "errors":   fields.Nested(api.model("NoError", {})),
        "message":  fields.String(default="Successfully Fetched Overview"),
        "overview": fields.Raw(   default='["DataCollection1 | 2009-05-12 10:11:12 | Updated: True","DataCollection2 | 2025-02-04 08:15:49 | Updated: False"]')
    })
    
    overview_failure_model = api.model("OverviewFailure", {
        "errors":   fields.Raw(   default='{"ErrorType": "ErrorMessage"}'),
        "message":  fields.String(default="Action aborted. Exception raised"),
        "overview": fields.Raw(   default="[]")
    })

    return {
        "success": overview_success_model,
        "failure": overview_failure_model
    }

def get_list_models(api) -> dict[str, object]:
    list_success_model = api.model("ListSuccess", {
        "errors":   fields.Nested(api.model("NoError", {})),
        "message":  fields.String(default="Successfully Fetched Overview"),
        "overview": fields.Raw(   default={
            "DataCollection1": {
                "description": "The best Collection", 
                "creation_date": "Today", 
                "modification_date": "13:58", 
                "updated": True
            },"DataCollection2": {
                "description": "The next best collection", 
                "creation_date": "1960", 
                "modification_date": "2080 1 January", 
                "updated": False
            }})
    })

    list_failure_model = api.model("ListFailure", {
        "errors":   fields.Raw(   default='{"ErrorType": "ErrorMessage"}'),
        "message":  fields.String(default="Action aborted. Exception raised"),
        "overview": fields.Raw(   default="{}")
    })

    return {
        "success": list_success_model,
        "failure": list_failure_model
    }

def get_info_models(api) -> dict[str, object]:
    info_success_model = api.model("InfoSuccess", {
        "errors":   fields.Nested(api.model("NoError", {})),
        "message":  fields.String(default="Successfully Fetched Info"),
        "info": fields.Raw(       default={
            "name": "DataCollection1", 
            "description": "The best Collection", 
            "creation_date": "Today", 
            "modification_date": "13:58", 
            "updated": True})
    })

    info_failure_model = api.model("InfoFailure", {
        "errors":   fields.Raw(   default='{"MissingParameter": "Parameter \"name\" is required"}'),
        "message":  fields.String(default="Action aborted. Exception raised"),
        "info": fields.Raw(       default="{}")
    })

    return {
        "success": info_success_model,
        "failure": info_failure_model
    }

def get_backup_models(api) -> dict[str, object]:
    backup_input_model = api.model("AddBackup", {
        "collection_name": fields.String(required=True, description="The unique name of the collection which the backup will be added to", default="Unique Name"),
        "backup_name":     fields.String(required=True, description="The unique name of the backup to be created", default="Unique Name"),
        "backup_location": fields.String(required=True, description="Location where the backup is stored", default="/home/user/backup.bak"),
        "backup_date":     fields.String(required=False, description="Optional backup date. Set to current time if not set", default="1960-06-01 15:31:10")
    }, strict=True)

    backup_success_model = api.model("AddBackupSuccess", {
        "errors":  fields.Nested(api.model("NoError", {})),
        "message": fields.String(default="Backup Created Successfully")
    })

    backup_failure_model = api.model("AddBackupFailure", {
        "errors":  fields.Raw(   default='{"BackupAlreadyExistsError": "BackupEntry with name \'backup_name\' already exists"}'),
        "message": fields.String(default="No Backup Was Created")
    })

    return {
        "input": backup_input_model,
        "success": backup_success_model,
        "failure": backup_failure_model
    }

def get_search_models(api) -> dict[str, object]:
    search_success_model = api.model("SearchSuccess", {
        "errors":   fields.Nested(api.model("NoError", {})),
        "message":  fields.String(default="Successfully Fetched Search Results"),
        "search": fields.Raw(     default={
            "DataCollection1": {
                "description": "The best Collection", 
                "creation_date": "Today", 
                "modification_date": "13:58", 
                "updated": True}})
    })

    search_failure_model = api.model("SearchFailure", {
        "errors":   fields.Raw(   default='{"MissingParameter": "Parameter \"name\" is required"}'),
        "message":  fields.String(default="Action aborted. Exception raised"),
        "search": fields.Raw(   default="{}")
    })

    return {
        "success": search_success_model,
        "failure": search_failure_model
    }

def get_edit_models(api) -> dict[str, object]:
    edit_input_model = api.model("EditCollection", {
        "collection_name":       fields.String(required=True, description="The unique name of the collection to be edited", default="Unique Name"),
        "name":                  fields.String(required=False, description="The new unique name of the collection", default="New Unique Name"),
        "description":           fields.String(required=False, description="The new description of the collection", default="New Description"),
        "creation_date":         fields.String(required=False, description="The new creation date of the collection", default="New Date"),
        "modification_date":     fields.String(required=False, description="The new modification date of the collection", default="New Date"),
        "updated":               fields.Boolean(required=False, description="Whether or not the collection is up to date", default=True)
    }, strict=True)

    edit_success_model = api.model("EditSuccess", {
        "errors":  fields.Nested(api.model("NoError", {})),
        "message": fields.String(default="Edit Was Successfull")
    })

    edit_failure_model = api.model("EditFailure", {
        "errors":  fields.Raw(   default='{"InvalidCollectionEditError": "Key \'key\' and associated value is not a valid edit"}'),
        "message": fields.String(default="No Edit Was Made")
    })

    return {
        "input": edit_input_model,
        "success": edit_success_model,
        "failure": edit_failure_model
    }

def get_unbackup_models(api) -> dict[str, object]:
    unbackup_input_model = api.model("UnBackup", {
        "collection_name":       fields.String(required=True, description="The unique name of the collection holding the backup to be deleted", default="Unique Name"),
        "backup_name":           fields.String(required=True, description="The unique name of the backup to delete", default="Unique Name")
    }, strict=True)

    unbackup_success_model = api.model("UnBackupSuccess", {
        "errors":  fields.Nested(api.model("NoError", {})),
        "message": fields.String(default="Deletion Was Successfull")
    })

    unbackup_failure_model = api.model("UnBackupFailure", {
        "errors":  fields.Raw(   default='{"BackupNotFoundError": "BackupEntry with name \'backup_name\' not found in `backup_entries`'),
        "message": fields.String(default="No Deletion Was Made")
    })

    return {
        "input": unbackup_input_model,
        "success": unbackup_success_model,
        "failure": unbackup_failure_model
    }

def get_delete_models(api) -> dict[str, object]:
    delete_success_model = api.model("DeleteSuccess", {
        "errors":   fields.Nested(api.model("NoError", {})),
        "message":  fields.String(default="Successfully Deleted DataCollection")
    })

    delete_failure_model = api.model("DeleteFailure", {
        "errors":   fields.Raw(   default='{"MissingParameter": "Parameter \"name\" is required"}'),
        "message":  fields.String(default="Action aborted. Exception raised")
    })

    return {
        "success": delete_success_model,
        "failure": delete_failure_model
    }

def get_listbackups_models(api) -> dict[str, object]:
    listbackups_success_model = api.model("ListBackupsSuccess", {
        "errors":         fields.Nested(api.model("NoError", {})),
        "message":        fields.String(default="Successfully Fetched a List of BackupEntries"),
        "backup_entries": fields.Raw(   default={
            "BackupEntry1": {
                "date": "1960", 
                "location": "/home/user/backup.bak"
            }, "BackupEntry2": {
                "date": "2015", 
                "location": "On top of the really big shelf"
            }
        })
    })

    listbackups_failure_model = api.model("ListBackupsFailure", {
        "errors":         fields.Raw(   default='{"MissingParameter": "Parameter \"name\" is required"}'),
        "message":        fields.String(default="Action aborted. Exception raised"),
        "backup_entries": fields.Raw(   default="{}")
    })

    return {
        "success": listbackups_success_model,
        "failure": listbackups_failure_model
    }
