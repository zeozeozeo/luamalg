/* don't forget to define LUA_IMPLEMENTATION or LUAMALG_IMPLEMENTATION in ONE .c
 * or .cpp file before including luamalg.h to create the implementation */
#define LUA_IMPLEMENTATION
#include "../luamalg.h"

int main(void) {
    lua_State* lua = luaL_newstate();
    luaL_openlibs(lua);
    luaL_dostring(lua, "print('Hello, World! (from Lua)')");
    lua_close(lua);
    return 0;
}
