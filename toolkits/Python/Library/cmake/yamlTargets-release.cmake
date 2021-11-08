#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "yaml" for configuration "Release"
set_property(TARGET yaml APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(yaml PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/yaml.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/yaml.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS yaml )
list(APPEND _IMPORT_CHECK_FILES_FOR_yaml "${_IMPORT_PREFIX}/lib/yaml.lib" "${_IMPORT_PREFIX}/bin/yaml.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
