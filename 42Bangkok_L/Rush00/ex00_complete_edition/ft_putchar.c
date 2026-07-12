/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putchar.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: miazanov <miazanov@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/08 16:04:26 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/12 18:58:51 by miazanov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	rush00(int x, int y);
void	rush01(int x, int y);
void	rush02(int x, int y);
void	rush03(int x, int y);
void	rush04(int x, int y);

void	ft_putchar(char c)
{
	write(1, &c, 1);
}

void	ft_putstr(char *str)
{
	int	i;

	i = 0;
	while (str[i] != '\0')
	{
		write(1, &str[i], 1);
		i++;
	}
}

// Validation check if it is number return 1, it isn't number return 0
int	ft_str_is_numeric(char *str)
{
	int	i;

	i = 0;
	while (str[i] != '\0')
	{
		if (!(str[i] >= '0' && str[i] <= '9'))
			return (0);
		i++;
	}
	return (1);
}

int	ft_nbr(char *s)
{
	int	nbr;
	int	i;

	i = 0;
	nbr = 0;
	while (s[i] != '\0')
	{
		{
			nbr = nbr * 10;
			nbr = nbr + (s[i] - '0');
		}
		i++;
	}
	return (nbr);
}

void	decision(int a, int x, int y)
{
	if (a == 0)
		rush00(x, y);
	else if (a == 1)
		rush01(x, y);
	else if (a == 2)
		rush02(x, y);
	else if (a == 3)
		rush03(x, y);
	else if (a == 4)
		rush04(x, y);
	else
		ft_putstr("The first digit must be 1, 2, 3 or 4!");
}
