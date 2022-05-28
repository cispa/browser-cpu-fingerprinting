def replace_uarch_by_base(uarchs):
    # Skylake
    uarchs = list(map(lambda x: "Skylake" if x == "Kaby Lake" else x, uarchs))
    uarchs = list(map(lambda x: "Skylake" if x == "Coffee Lake" else x, uarchs))
    uarchs = list(map(lambda x: "Skylake" if x == "Comet Lake" else x, uarchs))
    uarchs = list(map(lambda x: "Skylake" if x == "Whiskey Lake" else x, uarchs))

    # Haswell
    uarchs = list(map(lambda x: "Haswell" if x == "Broadwell" else x, uarchs))   

    # Sandy Bridge
    uarchs = list(map(lambda x: "Sandy Bridge" if x == "Ivy Bridge" else x, uarchs))

    # Sunny Cove
    uarchs = list(map(lambda x: "Sunny Cove" if x == "Ice Lake" else x, uarchs))

    # Willow Cove
    uarchs = list(map(lambda x: "Willow Cove" if x == "Tiger Lake" else x, uarchs))

    return uarchs