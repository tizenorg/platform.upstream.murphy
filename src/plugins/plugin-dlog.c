#include <stdlib.h>
#include <dlog.h>

#include <murphy/common.h>
#include <murphy/core.h>

#ifdef LOG_TAG
#undef LOG_TAG
#endif
#define LOG_TAG "murphyd"

/* Logger function */

static void dlogger(void *data, mrp_log_level_t level, const char *file,
                     int line, const char *func, const char *format, va_list ap)
{
    va_list cp;
    int     prio;
    char    fbuf[1024];

    MRP_UNUSED(data);

    va_copy(cp, ap);
    switch (level) {
    case MRP_LOG_ERROR:   prio = DLOG_ERROR;    break;
    case MRP_LOG_WARNING: prio = DLOG_WARN;     break;
    case MRP_LOG_INFO:    prio = DLOG_INFO;     break;
    case MRP_LOG_DEBUG:   prio = DLOG_DEBUG;    break;
    default:              prio = DLOG_INFO;
    }

    snprintf(fbuf, sizeof(fbuf), "%s: %s(%d) > %s", file, func, line, format);
	dlog_vprint(prio, LOG_TAG, fbuf, cp);

    va_end(cp);
}

/* Plugin initialization */

static int dlogger_init(mrp_plugin_t *plugin)
{
    MRP_UNUSED(plugin);

    if (mrp_log_register_target("dlog", dlogger, NULL))
        mrp_log_info("dlog: registered logging target.");
    else
        mrp_log_error("dlog: failed to register logging target.");

    return TRUE;
}

/* Plugin deinitialization */

static void dlogger_exit(mrp_plugin_t *plugin)
{
    MRP_UNUSED(plugin);

    mrp_log_unregister_target("dlog");

    return;
}

#define DLOGGER_DESCRIPTION "A dlog based logger for Murphy."
#define DLOGGER_HELP        "dlog logger support for Murphy."
#define DLOGGER_VERSION     MRP_VERSION_INT(0, 0, 1)
#define DLOGGER_AUTHORS     "Ievgen Vagin <i.vagin@samsung.com>"

MURPHY_REGISTER_PLUGIN("dlog",
                       DLOGGER_VERSION, DLOGGER_DESCRIPTION,
                       DLOGGER_AUTHORS, DLOGGER_HELP, MRP_SINGLETON,
                       dlogger_init, dlogger_exit,
                       NULL, 0, NULL, 0, NULL, 0, NULL);
