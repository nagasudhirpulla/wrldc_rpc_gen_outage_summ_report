select rto.ID as pwc_id,
    rto.ELEMENT_ID,
    rto.ELEMENTNAME,
    rto.ENTITY_ID,
    ent_master.ENTITY_NAME,
    gen_unit.installed_capacity,
    rto.OUTAGE_DATE,
    rto.REVIVED_DATE,
    rto.CREATED_DATE,
    rto.MODIFIED_DATE,
    sd_tag.name as shutdown_tag,
    rto.SHUTDOWN_TAG_ID,
    sd_type.name as shutdown_typeName,
    rto.SHUT_DOWN_TYPE,
    rto.OUTAGE_REMARKS,
    reas.reason,
    rto.REASON_ID,
    rto.REVIVAL_REMARKS,
    rto.REGION_ID,
    rto.SHUTDOWNREQUEST_ID,
    rto.IS_DELETED,
    rto.OUTAGE_TIME,
    rto.REVIVED_TIME
from real_time_outage rto
    left join outage_reason reas on reas.id = rto.reason_id
    left join shutdown_outage_tag sd_tag on sd_tag.id = rto.shutdown_tag_id
    left join shutdown_outage_type sd_type on sd_type.id = rto.shut_down_type
    left join entity_master ent_master on ent_master.id = rto.ENTITY_ID
    left join generating_unit gen_unit on gen_unit.id = rto.element_id
where rto.OUTAGE_DATE between :1 and :2
    or rto.revived_date between :1 and :2
    or rto.MODIFIED_DATE between :1 and :2
    or rto.CREATED_DATE between :1 and :2