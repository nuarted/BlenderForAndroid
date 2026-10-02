#include <SDL3/SDL.h>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <sys/stat.h>

extern int main(int, const char **);

extern "C" __attribute__((visibility("default"))) int SDL_main(int argc, char **argv)
{
  const char *storage = SDL_GetAndroidInternalStoragePath();
  if (!storage) return 1;
  const std::string root(storage);
  setenv("HOME", storage, 1);
  setenv("BLENDER_SYSTEM_DATAFILES", (root + "/blender/datafiles").c_str(), 1);
  setenv("BLENDER_USER_CONFIG", (root + "/config").c_str(), 1);
  mkdir((root + "/config").c_str(), 0700);
  if (FILE *log = std::fopen((root + "/blender.log").c_str(), "w")) std::fclose(log);
  std::freopen((root + "/blender.log").c_str(), "a", stdout);
  std::freopen((root + "/blender.log").c_str(), "a", stderr);
  std::setvbuf(stdout, nullptr, _IONBF, 0);
  std::setvbuf(stderr, nullptr, _IONBF, 0);
  return main(argc, const_cast<const char **>(argv));
}
