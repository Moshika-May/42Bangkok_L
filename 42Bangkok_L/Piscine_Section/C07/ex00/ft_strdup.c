/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/25 16:23:56 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/25 23:15:21 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

unsigned int	len(const char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

char	*ft_strdup(const char *src)
{
	unsigned int	i;
	char			*dest;

	i = 0;
	dest = malloc(sizeof(char) * (len(src) + 1));
	if (!dest)
		return (NULL);
	while (src[i])
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = '\0';
	return (dest);
}
