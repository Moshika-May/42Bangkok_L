/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_abs.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mbury <mbury@student.42bangkok.com>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/23 11:14:57 by mbury             #+#    #+#             */
/*   Updated: 2026/07/23 15:40:46 by mbury            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_ABS_H
# define FT_ABS_H
# include <limits.h>
# define ABS(value) ft_abs(value)

int	ft_abs(int value)
{
	if (value == INT_MIN)
		return (INT_MAX);
	else if (value < 0)
		return (value *= -1);
	else
		return (value);
}

#endif // FT_ABS_H