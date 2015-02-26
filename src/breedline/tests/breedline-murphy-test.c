/*
 * Copyright (c) 2012, Intel Corporation
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *
 *   * Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *   * Neither the name of Intel Corporation nor the names of its contributors
 *     may be used to endorse or promote products derived from this software
 *     without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

#include <murphy/common.h>

#include "breedline/breedline-murphy.h"

static void line_cb(brl_t *brl, const char *line, void *user_data)
{
    mrp_mainloop_t *ml = (mrp_mainloop_t *)user_data;

    MRP_UNUSED(brl);

    printf("got line: '%s'\n", line);

    if (!strcmp(line, "exit") || !strcmp(line, "quit"))
        mrp_mainloop_quit(ml, 0);
    else {
        if (brl_add_history(brl, line) != 0)
            fprintf(stderr, "Failed to save history entry.\n");
    }
}


int main(int argc, char *argv[])
{
    mrp_mainloop_t *ml;
    brl_t          *brl;
    int             fd;
    const char     *prompt;

    ml = mrp_mainloop_create();

    if (ml == NULL) {
        fprintf(stderr, "Failed to create mainloop.\n");
        exit(1);
    }

    fd     = fileno(stdin);
    prompt = argc > 1 ? argv[1] : "breedline-murphy";

    brl = brl_create_with_murphy(fd, prompt, ml, line_cb, ml);

    if (brl == NULL) {
        fprintf(stderr, "Failed to create breedline context (%d: %s).\n",
                errno, strerror(errno));
        exit(1);
    }

    brl_show_prompt(brl);
    mrp_mainloop_run(ml);
    brl_destroy(brl);
    mrp_mainloop_destroy(ml);

    return 0;
}
