
statement_create_vfx_shots = \
	"""
	CREATE TABLE IF NOT EXISTS "vfx_shots" (
		"id"	INTEGER NOT NULL,
		"vfx_id"	TEXT NOT NULL UNIQUE,
		"date_added"	NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY("id" AUTOINCREMENT)
	)
	"""


statement_create_snapshots = \
	"""
	CREATE TABLE IF NOT EXISTS "snapshots" (
		"id"	INTEGER NOT NULL,
		"snapshot_name"	TEXT NOT NULL,
		"date_added"	NUMERIC DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY("id" AUTOINCREMENT)
	)
	"""


statement_create_timelines = \
	"""
	CREATE TABLE IF NOT EXISTS "timelines" (
		"id"	INTEGER NOT NULL,
		"snapshot_id"	INTEGER NOT NULL,
		"name"	TEXT NOT NULL,
		"start_frames"	INTEGER NOT NULL CHECK("start_frames" > 0),
		"date_added"	NUMERIC DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY("id" AUTOINCREMENT),
		FOREIGN KEY("snapshot_id") REFERENCES "snapshots"("id") ON UPDATE CASCADE ON DELETE CASCADE
	)
	"""

statement_create_vfx_shot_instances = \
	"""
	CREATE TABLE IF NOT EXISTS "vfx_shot_instances" (
		"id"	INTEGER NOT NULL,
		"vfx_shot_id"	INTEGER NOT NULL,
		"timeline_id"	INTEGER NOT NULL,
		"timeline_start_offset"	INTEGER NOT NULL CHECK(timeline_start_offset > 0),
		"duration"	INTEGER NOT NULL CHECK(duration > 0),
		"date_added"	NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY("id" AUTOINCREMENT),
		FOREIGN KEY("timeline_id") REFERENCES "timelines"("id") ON UPDATE CASCADE ON DELETE CASCADE,
		FOREIGN KEY("vfx_shot_id") REFERENCES "vfx_shots"("id") ON UPDATE CASCADE ON DELETE CASCADE
	)
	"""

statement_create_plate_instances = \
	"""
	CREATE TABLE IF NOT EXISTS "plate_instances" (
		"id"	INTEGER NOT NULL,
		"vfx_shot_instance_id"	INTEGER NOT NULL,
		"vfx_shot_instance_offset"	INTEGER NOT NULL CHECK(vfx_shot_instance_offset > 0),
		"track_index"	INTEGER NOT NULL CHECK(track_index > 0),
		"source_name"	TEXT NOT NULL,
		"source_in"	INTEGER NOT NULL CHECK(source_in >= 0),
		"source_duration"	INTEGER NOT NULL CHECK(source_duration > 0),
		"is_muted"	INTEGER NOT NULL DEFAULT 0 CHECK(is_muted in(0,1)),
		PRIMARY KEY("id" AUTOINCREMENT),
		FOREIGN KEY("vfx_shot_instance_id") REFERENCES "vfx_shot_instances"("id") ON UPDATE CASCADE ON DELETE CASCADE
	)
	"""