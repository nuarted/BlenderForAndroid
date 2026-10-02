OpenEXR port copied from vcpkg commit 3aea538b2bb21a586502c67b00eb474fdd2e3098.

The only port change applies android-api26-allocation.patch: use posix_memalign
for the Zstd shuffle buffer on Android below API 28. It preserves 64-byte
alignment, allocation failure handling, and compatibility with free().
