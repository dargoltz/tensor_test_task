CREATE TYPE hierarchy_item_type AS ENUM ('1', '2', '3');

CREATE TABLE hierarchy_items
(
    id        BIGSERIAL PRIMARY KEY,
    parent_id BIGINT              NULL REFERENCES hierarchy_items (id) ON DELETE CASCADE,
    name      TEXT                NOT NULL,
    type      hierarchy_item_type NOT NULL,

    -- организация не имеет родителя
    CONSTRAINT chk_org_has_no_parent
        CHECK (type <> '1' OR parent_id IS NULL),

    -- отдел обязан иметь родителя
    CONSTRAINT chk_dep_has_parent
        CHECK (type <> '2' OR parent_id IS NOT NULL),

    -- сотурдник обязан иметь родителя
    CONSTRAINT chk_emp_has_parent
        CHECK (type <> '3' OR parent_id IS NOT NULL)
);
