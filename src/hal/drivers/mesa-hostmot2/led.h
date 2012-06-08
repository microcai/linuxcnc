
//    Copyright (C) 2012 Michael Geszkiewicz
//
//    This program is free software; you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation; either version 2 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program; if not, write to the Free Software
//    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
//

#ifndef __LED_H
#define __LED_H

typedef struct {
    hal_bit_t *led;
} hm2_led_instance_t ;

typedef struct {
    int num_instances ;
    hm2_led_instance_t *instance;

    u32 written_buff ;

    u32 led_addr;
    u32 *led_reg;
} hm2_led_t ;

int hm2_led_parse_md(hostmot2_t *hm2, int md_index);

#endif