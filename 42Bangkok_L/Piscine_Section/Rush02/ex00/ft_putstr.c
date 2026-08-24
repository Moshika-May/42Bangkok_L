/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ataweech <ataweech@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 19:47:32 by ataweech          #+#    #+#             */
/*   Updated: 2026/07/26 19:47:33 by ataweech         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rush02.h"

void	ft_putstr(char *str)
{
	unsigned int	i;

	if (!str)
		return ;
	i = 0;
	while (str[i])
	{
		write(1, &str[i], 1);
		i++;
	}
	return ;
}
