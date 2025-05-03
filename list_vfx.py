import sys, uuid
import avb, avbutils

VFX_IDS_TRACK_LABEL = "VFX IDs"
"""Label given to the track containing  VFX ID subcaps"""

UUID_SUBCAP_TEXT = uuid.UUID("bac7f4c7-7eeb-4898-be2c-085f07113cc5")
#UUID_SUBCAP_TEXT = uuid.UUID("3319f04a-ac69-4525-b9e8-2206362fd233")	# This one shows up too?

def get_subcap_caption(track_effect:avb.trackgroups.TrackEffect):

	for param in track_effect.param_list:
		if isinstance(param.value, avb.misc.CFUserParam):
			user_param = param.value
			if user_param.uuid == UUID_SUBCAP_TEXT:
				return user_param.data.decode("utf-8")



if __name__ == "__main__":

	if not len(sys.argv) > 1:
		import pathlib
		print(f"Usage: {pathlib.Path(__file__).name} reel.avb", file=sys.stderr)
		sys.exit(1)
	

	with avb.open(sys.argv[1]) as bin_handle:

		bin_contents = bin_handle.content

		# Get top timeline
		timelines = avbutils.get_timelines_from_bin(bin_contents)
		first_timeline = next(timelines)
		timeline_timecode = avbutils.get_timecode_range_for_composition(first_timeline)
		print(first_timeline.name)
		
		# Get VFX Subcap track (track labeled "VFX IDs")
		vfx_track = next(t 
			for t in avbutils.get_tracks_from_composition(first_timeline, avbutils.TrackTypes.PICTURE)
			if "attributes" in t.property_data
			and t.attributes.get("_COMMENT","").lower() == VFX_IDS_TRACK_LABEL.lower()
		)

		# Get dailies/plates track (V1)
		dailies_track = next(avbutils.get_tracks_from_composition(first_timeline, avbutils.TrackTypes.PICTURE, index=1))
		
		components = avbutils.get_components_from_track_component(vfx_track.component)
		
		tc_current = timeline_timecode.start
		for component in components:
			
			if not isinstance(component, avb.components.Filler):

				if "attributes" not in component.property_data or "_EFFECT_PLUGIN_NAME" not in component.attributes:
					print("Unknown attributes")
				if not component.attributes["_EFFECT_PLUGIN_NAME"].lower() == "subcap":
					print("Not Subclip")
				
				subcap_text = get_subcap_caption(component)

				print(f"{tc_current} - {tc_current + component.length}\t{subcap_text}")
			
			tc_current += component.length