/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strcapitalize.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/14 10:06:20 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/14 13:37:43 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// #include <stdio.h>

char	make_low_case(char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i] != '\0')
	{
		if (str[i] >= 'A' && str[i] <= 'Z')
			str[i] += 32;
		i++;
	}
	return (*str);
}

char	*ft_strcapitalize(char *str)
{
	unsigned int	i;
	unsigned int	j;

	i = 0;
	j = 0;
	make_low_case(str);
	while (str[i] != '\0')
	{
		if (str[i] < 'a' || str[i] > 'z')
		{
			if (str[i] >= '0' && str[i] <= '9')
				j++;
			else
				j = 0;
		}
		if ((str[i] >= 'a' && str[i] <= 'z') && j == 0)
		{
			str[i] -= 32;
			j++;
		}
		else if (str[i] >= 'a' && str[i] <= 'z')
			j++;
		i++;
	}
	return (str);
}
/*
int	main(void)
{
	char	txt[] = "hi, how are you? 42words forty-two; fifty+and+one YEAH thIs also NeeD";

	printf("%s", ft_strcapitalize(txt));
	return (0);
}
*/
