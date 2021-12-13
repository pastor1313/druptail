SELECT
    n1.nid AS article_id,
    n2.body_value AS article_body,
    n3.title AS title
FROM node n1
    LEFT JOIN node__body n2
        ON n1.nid = n2.entity_id
    LEFT JOIN node_field_data n3
        ON n1.nid = n3.nid
