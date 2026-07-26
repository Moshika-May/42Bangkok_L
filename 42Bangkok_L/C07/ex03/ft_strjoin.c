/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 11:53:58 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/26 13:20:23 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>
#include <stdlib.h>

unsigned int	len(const char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i])
	{
		i++;
	}
	return (i);
}

unsigned int	len_all_cal(int size, char **strs, char *sep)
{
	unsigned int	len_sum;
	unsigned int	i;

	len_sum = 0;
	i = 0;
	while (i < (unsigned int)size)
	{
		len_sum += len(strs[i]);
		i++;
	}
	len_sum += len(sep) * (size - 1);
	return (len_sum);
}

char	*put_in_array(char *dest, int size, char **strs, char *sep)
{
	unsigned int	i;
	unsigned int	j;
	unsigned int	k;

	i = 0;
	k = 0;
	while (i < (unsigned int)size)
	{
		j = 0;
		while (strs[i][j] != '\0')
		{
			dest[k++] = strs[i][j++];
		}
		if (i < (unsigned int)size - 1)
		{
			j = 0;
			while (sep[j] != '\0')
			{
				dest[k++] = sep[j++];
			}
		}
		i++;
	}
	dest[k] = '\0';
	return (dest);
}

char	*ft_strjoin(int size, char **strs, char *sep)
{
	char			*dest;
	unsigned int	len_all;

	if (size == 0)
	{
		dest = (char *)malloc(sizeof(char) * (size + 1));
		if (!dest)
			return (NULL);
		dest[size] = '\0';
		return (dest);
	}
	len_all = len_all_cal(size, strs, sep);
	dest = (char *)malloc(sizeof(char) * (len_all + 1));
	if (!dest)
		return (NULL);
	dest = put_in_array(dest, size, strs, sep);
	return (dest);
}
/*
#include <stdio.h>

int	main(void)
{
	char	*word[] = {"Hello", "world!", "this", "is", "C"};
	char	*separator;
	char	*joined_string;

	separator = " *** ";
	joined_string = ft_strjoin(5, word, separator);
	printf("%s\n", joined_string);
	free(joined_string);
	joined_string = ft_strjoin(0, word, separator);
	printf("%s\n", joined_string);
	free(joined_string);
	return (0);
}
*/
