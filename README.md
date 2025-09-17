How to use:

    DataManager store;
    
    // Load Data
    store.load("file.data");

    // Create / Update
    store.set("username", "mndfq");

    // Read
    std::cout << store.get("username");

    // Is it real?
    if (store.exists("level")) {
        std::cout << store.get("level") << "\n";
    }

    // Delete
    store.remove("level");

    // List all keys
    for (const auto& key : store.keys()) {
        std::cout << "Key: " << key << " -> " << store.get(key) << "\n";
    }

    // Save
    store.save("file.data");
