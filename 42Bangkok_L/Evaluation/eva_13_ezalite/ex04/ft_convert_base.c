/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_convert_base.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ezalite <ezalite@student.42bangkok>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/22 13:01:35 by ezalite           #+#    #+#             */
/*   Updated: 2026/07/24 22:19:49 by ezalite          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

int	ft_base_is_valid(char *base)
{
	int	i;
	int	j;

	i = 0;
	while (base[i])
	{
		if (base[i] < ' ' || '~' < base[i]
			|| base[i] == '+' || base[i] == '-')
			return (0);
		i++;
	}
	if (i < 2)
		return (0);
	i = 0;
	while (base[i])
	{
		j = i + 1;
		while (base[j])
			if (base[i] == base[j++])
				return (0);
		i++;
	}
	return (1);
}

int	ft_atoi_base(char *nbr, char *base, int b)
{
	int	nb;
	int	sign;
	int	i;

	sign = 1;
	nb = 0;
	while (('\t' <= *nbr && *nbr <= '\r') || *nbr == ' ')
		nbr++;
	while (*nbr == '+' || *nbr == '-')
		sign *= ',' - *nbr++;
	while (*nbr)
	{
		i = 0;
		while (*nbr != base[i] && base[i])
			i++;
		if (base[i] == '\0')
			break ;
		nb = nb * b + sign * i;
		nbr++;
	}
	return (nb);
}

char	*ft_nbr2base_string(int nbr, char *base_to, char *nbr_base, int size)
{
	int	base;
	int	sign;

	base = 0;
	while (base_to[base])
		base++;
	sign = 1;
	if (nbr < 0)
		sign = -1;
	while (size > 1)
	{
		nbr_base[size - 1] = base_to[sign * (nbr % base)];
		nbr /= base;
		size--;
	}
	if (sign == 1)
		nbr_base[0] = base_to[nbr % base];
	else
		nbr_base[0] = '-';
	return (nbr_base);
}

char	*ft_to_base(int nbr, char *base_to)
{
	int		nbr_cpy;
	int		base;
	int		i;
	char	*nbr_base;

	base = 0;
	while (base_to[base])
		base++;
	i = 1;
	if (nbr < 0)
		i++;
	nbr_cpy = nbr;
	while (nbr_cpy / base != 0)
	{
		nbr_cpy /= base;
		i++;
	}
	nbr_base = malloc(sizeof (char) * i + 1);
	if (nbr_base == NULL)
		return (NULL);
	nbr_base[i] = '\0';
	nbr_base = ft_nbr2base_string(nbr, base_to, nbr_base, i);
	return (nbr_base);
}

char	*ft_convert_base(char *nbr, char *base_from, char *base_to)
{
	int		b;
	int		nbr_int;
	char	*nbr_base;

	if (!ft_base_is_valid(base_from) || !ft_base_is_valid(base_to))
		return (NULL);
	b = 0;
	while (base_from[b])
		b++;
	nbr_int = ft_atoi_base(nbr, base_from, b);
	nbr_base = ft_to_base(nbr_int, base_to);
	if (nbr_base == NULL)
		return (NULL);
	return (nbr_base);
}
/*
#include <stdio.h>

int	main(void)
{
	printf("%s\n", ft_convert_base("	---1003", "0123", "0123456789"));
	printf("%d\n", ft_atoi_base("	---1003", "012", 3));
	return (0);
}*/
