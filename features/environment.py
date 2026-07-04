def after_scenario(context, scenario):
    temp_dir = getattr(context, "bdd_tmpdir", None)
    if temp_dir:
        temp_dir.cleanup()
