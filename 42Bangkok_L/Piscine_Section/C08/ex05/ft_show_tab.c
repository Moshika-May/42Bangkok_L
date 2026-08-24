/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_show_tab.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 21:47:16 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/29 23:18:08 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_stock_str.h"
#include <unistd.h>

void	ft_putstr(char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i])
	{
		write(1, &str[i], 1);
		i++;
	}
}

int	cond_check(long n)
{
	if (n < 0)
	{
		write(1, "-", 1);
		return (0);
	}
	if (n == 0)
	{
		write(1, "0", 1);
		return (1);
	}
	return (0);
}

void	ft_putnbr(int nb)
{
	char			b[20];
	unsigned int	i;
	long			n;

	n = nb;
	i = 0;
	if (cond_check(n) == 1)
		return ;
	if (n < 0)
		n = -n;
	while (n > 0)
	{
		b[i] = (n % 10) + '0';
		n /= 10;
		i++;
	}
	while (i > 0)
	{
		i--;
		write(1, &b[i], 1);
	}
}

void	ft_show_tab(struct s_stock_str *par)
{
	unsigned int	i;

	i = 0;
	while (par[i].str != 0)
	{
		ft_putstr(par[i].str);
		ft_putstr("\n");
		ft_putnbr(par[i].size);
		ft_putstr("\n");
		ft_putstr(par[i].copy);
		ft_putstr("\n");
		i++;
	}
}
