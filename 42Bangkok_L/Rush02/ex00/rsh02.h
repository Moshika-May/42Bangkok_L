/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rsh02.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/24 21:46:42 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/24 23:55:26 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef RSH02_H
# define RSH02_H

# include <fcntl.h>
# include <stdlib.h>
# include <unistd.h>

int					input_validation(int argc, char **argv);
void				putstr(char *str);
int					len(char *str);
unsigned long long	atoull(char *str);

#endif
