from PyAltium365.AltiumApi import AltiumApi
from PyAltium365.Connections.JsonConSearchAsync import JsonConSearchAsync
from PyAltium365.Data.DataConPortal import PrtGlobalServiceName, PrtSettings
from PyAltium365.Data.DataConSearchAsync import AsyncSearchObject, DataType, SearchDataType

api = AltiumApi()

api.login("email", "pass")
workspaces = api.get_user_workspaces()
api.workspace_login(workspaces[0], "email", "pass")

so = api.create_search_object()
#so.add_search_parameter_range("Value", 1e-10, 3e-10, DataType.CAPACITANCE, True, True)
so.add_search_content_type(SearchDataType.COMPONENT)
so.add_search_parameter("LatestRevision", "1")
#so.add_search_parameter("FolderFullPath", "Components\\Miscellaneous\\")
# so.add_search_parameter("ContentType", "layerstack")
# so.add_search_parameter("ContentType", "script")
print(so.get_current_count())
# p = so.get_all_search_names()
# print(p)
# temp = api._service_vault.get_alu_items(api._seswork_guid)
results = so.get_results(10)
# temp = {}
# for result in results:
#     for param in result.Parameters:
#         if param in temp:
#             temp[param] += 1
#         else:
#             temp[param] = 1
item = results[1].get_item()

lcd = item.get_life_cycle_definition()
item_r = item.get_latest_item_revision()

l = item_r.get_child_item_revisions()

print(item.HRID)
print(l)

# headers = {
#     'Accept': 'application/json',
#     'Authorization': f'AFSSessionID {api._seswork_guid}',
#     'host': 'magics-instruments-nv.365.altium.com',
#     'content-type': 'application/json; charset=utf-8',
#     'User-Agent': "Altium Designer"
# }
# response  = api._session.request('REPORT', 'https://magics-instruments-nv.365.altium.com/search/v1.0/searchasync',
#                              data='{"request":{"$type":"SearchRequest","Condition":{"$type":"DtoSearchConditionBooleanQuery","Items":[{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"ContentTypeDD420E8DDD8B445E911A0601BB2B6D53","Value":"Component"}},"Occur":0},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionWildcardQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"IdC623975962814A5FAAD7FA1CD85DA0DB","Value":"r_"}},"Occur":0},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionBooleanQuery","Items":[]},"Occur":0},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LatestRevisionDD420E8DDD8B445E911A0601BB2B6D53","Value":"1"}},"Occur":0},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"3687106a-bccc-4460-859a-1ffa4771a2bf"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"5742fd7b-36e8-436e-8a92-ea4ccd15ac16"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"5f91888b-0c38-4b87-a7ac-67e6e0b77675"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"62b8ab69-b661-47b0-8f22-547bcb2c7653"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"818172ab-3757-448b-bcf5-3d769e2e8523"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"ac9973a4-2e91-453a-965b-7bd042690bfd"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"b68aac75-c12f-458a-97bd-a0d73f2e3ff6"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"fa035d0e-638f-4f74-b9f5-41b92f2e4391"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"IsActiveC623975962814A5FAAD7FA1CD85DA0DB","Value":"0"}},"Occur":2}]},"SortFields":[{"$type":"DtoSortSearchField","Name":"LifeCycleDD420E8DDD8B445E911A0601BB2B6D53","Order":0}],"ReturnFields":null,"Start":0,"Limit":1,"IncludeFacets":false,"UseOnlyBestFacets":false,"IncludeDebugInfo":false,"IgnoreCaseFieldNames":false}}',
#                              headers=headers)
#
# response2 = api._session.request('REPORT', 'https://magics-instruments-nv.365.altium.com/search/v1.0/searchasync',
#                              data='{"request":{"$type":"SearchRequest","Condition":{"$type":"DtoSearchConditionBooleanQuery","Items":[{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionWildcardQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"IdC623975962814A5FAAD7FA1CD85DA0DB","Value":"r_"}},"Occur":0},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionBooleanQuery","Items":[]},"Occur":0},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LatestRevisionDD420E8DDD8B445E911A0601BB2B6D53","Value":"1"}},"Occur":0},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"3687106a-bccc-4460-859a-1ffa4771a2bf"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"5742fd7b-36e8-436e-8a92-ea4ccd15ac16"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"5f91888b-0c38-4b87-a7ac-67e6e0b77675"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"62b8ab69-b661-47b0-8f22-547bcb2c7653"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"818172ab-3757-448b-bcf5-3d769e2e8523"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"ac9973a4-2e91-453a-965b-7bd042690bfd"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"b68aac75-c12f-458a-97bd-a0d73f2e3ff6"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"LifeCycleStateGUIDC623975962814A5FAAD7FA1CD85DA0DB","Value":"fa035d0e-638f-4f74-b9f5-41b92f2e4391"}},"Occur":2},{"$type":"DtoSearchConditionBooleanQueryItem","Item":{"$type":"DtoSearchConditionStrictQuery","Term":{"$type":"DtoSearchConditionTerm","Field":"IsActiveC623975962814A5FAAD7FA1CD85DA0DB","Value":"0"}},"Occur":2}]},"SortFields":[{"$type":"DtoSortSearchField","Name":"LifeCycleDD420E8DDD8B445E911A0601BB2B6D53","Order":0}],"ReturnFields":null,"Start":0,"Limit":1,"IncludeFacets":false,"UseOnlyBestFacets":false,"IncludeDebugInfo":false,"IgnoreCaseFieldNames":false}}',
#                              headers=headers)
#
# response3 = api._session.request('REPORT', 'https://magics-instruments-nv.365.altium.com/search/v1.0/searchasync',
#                              data='{"request": {"$type": "SearchRequest","Condition": {"$type": "DtoSearchConditionBooleanQuery","Items": []},"SortFields": [],"ReturnFields": [],"Start": 0,"Limit": 0,"IncludeFacets": true,"UseOnlyBestFacets": true,"IncludeDebugInfo": false,"IgnoreCaseFieldNames": false}}',
#                              headers=headers)


# print(response.text)
# print(response2.text)
# print(json.loads(response3.content.decode('utf-8-sig')))

exit(0)

print(api._service_vault.get_alu_vault_record(api._seswork_guid))
print(api._service_vault.get_alu_items(api._seswork_guid))
print(api._service_vault.get_alu_tags(api._seswork_guid))
print(api._service_vault.get_alu_life_cycle_state(api._seswork_guid))
print(api._service_vault.get_alu_item_revision(api._seswork_guid))

api.get_prt_setting(PrtSettings.CIIVA_USER_NAME)

print(api.get_prt_setting(PrtSettings.CIIVA_PASSWORD))
print(api.get_prt_service_url(PrtGlobalServiceName.A365_VALIDATESESION))
print(api.get_user_workspaces()[0].get_owner_account())


licenses, gla, groups = api._portal_con.get_lic_available_licences_for_contact(api._session_guid)

print(api.check_adw_account_license())

print(licenses[1].get_created_by_user())
print(licenses[1].get_contact_user())
print(licenses[1].get_last_modified_by_user())
print(licenses[0].get_owner_account())
u1 = api.get_contact_details(licenses[1].CreatedByGUID)
u2 = api.get_contact_details(licenses[1].LastModifiedByGUID)
u3 = api.get_contact_details(licenses[1].ContactGUID)


print(u1)
