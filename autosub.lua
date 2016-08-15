-- default keybinding: b
-- add the following to your input.conf to change the default keybinding:
-- keyname script_binding auto_load_subs
local utils = require 'mp.utils'
function load_sub_fn()
    subtitle_path = get_script_path() .. "subtitle.py"
    local path = mp.get_property("path")
    mp.msg.info("Searching subtitle")
    mp.osd_message("Searching subtitle")
    res = utils.subprocess({args = {"python", subtitle_path, path, "--lang", "Chn"}})
    if res.status == 0 then
        mp.commandv("rescan_external_files", "reselect")
        mp.msg.info("Subtitle download succeeded")
        mp.osd_message("Subtitle download succeeded")
    else
        mp.msg.warn("Subtitle download failed")
        mp.osd_message(res.stdout)
    end
end


function get_script_path()
   local str = debug.getinfo(2, "S").source:sub(2)
   return str:match("(.*/)")
end



mp.add_key_binding("b", "auto_load_subs", load_sub_fn)
