#pragma once
#include <string>
#include <unordered_map>
#include <vector>
#include <fstream>
#include <sstream>
#include <iostream>
#include <stdexcept>

class DataManager {
public:
    // Load/save .dmb files
    bool load(const std::string& filename);
    bool save(const std::string& filename) const;

    // CRUD
    void setValue(const std::string& section, const std::string& key, const std::string& value);
    std::string getValue(const std::string& section, const std::string& key, const std::string& defaultValue="") const;
    bool removeKey(const std::string& section, const std::string& key);
    bool removeSection(const std::string& section);
    bool keyExists(const std::string& section, const std::string& key) const;
    bool sectionExists(const std::string& section) const;

    // Type-safe getters
    int getInt(const std::string& section, const std::string& key, int defaultValue=0) const;
    float getFloat(const std::string& section, const std::string& key, float defaultValue=0.0f) const;
    bool getBool(const std::string& section, const std::string& key, bool defaultValue=false) const;

    // Helpers
    std::vector<std::string> listSections() const;
    std::vector<std::string> listKeys(const std::string& section) const;
    void clearSection(const std::string& section);
    void clearAll();

private:
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> data_;

    static std::string trim(const std::string& s);
};
