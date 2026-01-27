#include "datamanager.h"

// ------------------- UTILITY -------------------
std::string DataManager::trim(const std::string& s) {
    const char* ws = " \t\n\r";
    size_t start = s.find_first_not_of(ws);
    if (start == std::string::npos) return "";
    size_t end = s.find_last_not_of(ws);
    return s.substr(start, end - start + 1);
}

// ------------------- LOAD -------------------
bool DataManager::load(const std::string& filename) {
    std::ifstream in(filename);
    if (!in.is_open()) return false;

    data_.clear();
    std::string line;
    std::string current_section;

    while (std::getline(in, line)) {
        line = trim(line);
        if (line.empty() || line[0] == '#') continue;

        if (line.front() == '[' && line.back() == ']') {
            current_section = line.substr(1, line.size()-2);
            continue;
        }

        size_t eq = line.find('=');
        if (eq == std::string::npos) {
            std::cerr << "Malformed line ignored: " << line << "\n";
            continue;
        }

        std::string key = trim(line.substr(0, eq));
        std::string value = trim(line.substr(eq+1));

        // Multi-line support <<< >>> (optional)
        if (value == "<<<") {
            std::ostringstream oss;
            while (std::getline(in, line)) {
                if (trim(line) == ">>>") break;
                oss << line << "\n";
            }
            value = oss.str();
        }

        data_[current_section][key] = value;
    }

    return true;
}

// ------------------- SAVE -------------------
bool DataManager::save(const std::string& filename) const {
    std::ofstream out(filename);
    if (!out.is_open()) return false;

    for (const auto& [section, keys] : data_) {
        out << "[" << section << "]\n";
        for (const auto& [key, value] : keys) {
            if (value.find('\n') != std::string::npos) {
                out << key << "=<<<\n" << value << ">>>\n";
            } else {
                out << key << "=" << value << "\n";
            }
        }
        out << "\n";
    }
    return true;
}

// ------------------- CRUD -------------------
void DataManager::setValue(const std::string& section, const std::string& key, const std::string& value) {
    data_[section][key] = value;
}

std::string DataManager::getValue(const std::string& section, const std::string& key, const std::string& defaultValue) const {
    auto sec = data_.find(section);
    if (sec == data_.end()) return defaultValue;
    auto it = sec->second.find(key);
    return it != sec->second.end() ? it->second : defaultValue;
}

bool DataManager::removeKey(const std::string& section, const std::string& key) {
    auto sec = data_.find(section);
    if (sec == data_.end()) return false;
    return sec->second.erase(key) > 0;
}

bool DataManager::removeSection(const std::string& section) {
    return data_.erase(section) > 0;
}

bool DataManager::keyExists(const std::string& section, const std::string& key) const {
    auto sec = data_.find(section);
    if (sec == data_.end()) return false;
    return sec->second.find(key) != sec->second.end();
}

bool DataManager::sectionExists(const std::string& section) const {
    return data_.find(section) != data_.end();
}

// ------------------- TYPE-SAFE GETTERS -------------------
int DataManager::getInt(const std::string& section, const std::string& key, int defaultValue) const {
    std::string v = getValue(section, key, "");
    if (v.empty()) return defaultValue;
    try { return std::stoi(v); } catch(...) { return defaultValue; }
}

float DataManager::getFloat(const std::string& section, const std::string& key, float defaultValue) const {
    std::string v = getValue(section, key, "");
    if (v.empty()) return defaultValue;
    try { return std::stof(v); } catch(...) { return defaultValue; }
}

bool DataManager::getBool(const std::string& section, const std::string& key, bool defaultValue) const {
    std::string v = getValue(section, key, "");
    if (v.empty()) return defaultValue;
    if (v == "true" || v == "1") return true;
    if (v == "false" || v == "0") return false;
    return defaultValue;
}

// ------------------- HELPERS -------------------
std::vector<std::string> DataManager::listSections() const {
    std::vector<std::string> sections;
    for (const auto& [sec,_] : data_) sections.push_back(sec);
    return sections;
}

std::vector<std::string> DataManager::listKeys(const std::string& section) const {
    std::vector<std::string> keys;
    auto sec = data_.find(section);
    if (sec != data_.end()) {
        for (const auto& [key,_] : sec->second) keys.push_back(key);
    }
    return keys;
}

void DataManager::clearSection(const std::string& section) {
    auto sec = data_.find(section);
    if (sec != data_.end()) sec->second.clear();
}

void DataManager::clearAll() {
    data_.clear();
}
